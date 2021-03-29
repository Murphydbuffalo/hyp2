from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4
from os import environ


class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self):
        return self.name


class HypUser(AbstractUser):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True)
    deactivated_at = models.DateTimeField('deactivated at', null=True, blank=True)

    def __str__(self):
        return self.email


def create_access_token():
    return uuid4().hex


class ApiKeyManager(models.Manager):
    def active(self):
        return self.get(deactivated_at=None)


class ApiKey(models.Model):
    access_token = models.UUIDField(default=create_access_token)
    label = models.CharField(max_length=200)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)
    deactivated_at = models.DateTimeField('deactivated at', null=True, blank=True)
    last_used_at = models.DateTimeField('last used at', null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    objects = ApiKeyManager()

    class Meta:
        indexes = [
            models.Index(fields=["access_token", "deactivated_at", "customer_id"])
        ]

        constraints = [
            models.UniqueConstraint(
                name="uniq_active_key_per_customer",
                fields=["customer_id"],
                condition=models.Q(deactivated_at=None),
            )
        ]

    def __str__(self):
        sandbox = environ.get("SANDBOX") == "ON"
        return f'{"SANDBOX" if sandbox else "PRODUCTION"}/HYP/{self.access_token}'


class Experiment(models.Model):
    name = models.CharField(max_length=200)
    stopped = models.BooleanField(default=False)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["name", "stopped", "customer_id"])
        ]

    def __str__(self):
        return self.name


class VariantInteractionCountManager(models.Manager):
    def with_interaction_counts(self):
        return self.annotate(
            num_interactions=models.Count("interaction"),
            num_conversions=models.Count(
                "interaction", filter=models.Q(interaction__converted=True)
            )
        )


class Variant(models.Model):
    objects = VariantInteractionCountManager()

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="uniq_variant_name_per_experiment",
                fields=["experiment_id", "name"]
            )
        ]

    def __str__(self):
        return self.name


class Interaction(models.Model):
    converted = models.BooleanField(default=False)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    participant_id = models.CharField(max_length=200)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["customer_id", "experiment_id", "participant_id", "variant_id"])
        ]

        constraints = [
            models.UniqueConstraint(
                name="uniq_interaction_per_experiment_and_participant",
                fields=["experiment_id", "participant_id"]
            )
        ]

    def __str__(self):
        return (
            f'Experiment {self.experiment_id}, Variant {self.variant_id},'
            f' Participant {self.participant_id}. Converted? {self.converted}'
        )
