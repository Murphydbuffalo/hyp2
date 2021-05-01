from django.contrib.auth.models import AbstractUser
from django.db import models, connection
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


class ApiKey(models.Model):
    access_token = models.UUIDField(default=create_access_token)
    label = models.CharField(max_length=200)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)
    deactivated_at = models.DateTimeField('deactivated at', null=True, blank=True)
    last_used_at = models.DateTimeField('last used at', null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=["access_token", "deactivated_at", "customer_id"])
        ]

    def description(self):
        return f'{self.label}: {self} {"" if self.is_active() else "(Deactivated)"}'

    def is_active(self):
        return self.deactivated_at is None

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


class VariantManager(models.Manager):
    def for_assignment(self, participant_id, access_token, experiment_id):
        return self.raw("""
        SELECT v.id, v.name, v.num_interactions, v.num_conversions, i.id as interaction_id
        FROM hyp_variant as v
        INNER JOIN hyp_apikey as k ON k.customer_id = v.customer_id
        LEFT OUTER JOIN hyp_interaction as i ON i.variant_id = v.id AND i.participant_id = %s
        WHERE k.access_token = %s AND k.deactivated_at IS NULL AND v.experiment_id = %s;
        """, [participant_id, access_token, experiment_id])


class Variant(models.Model):
    objects = VariantManager()
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # Counter cache fields
    num_interactions = models.IntegerField(default=0)
    num_conversions = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["customer_id", "experiment_id"])
        ]
        constraints = [
            models.UniqueConstraint(
                name="uniq_variant_name_per_experiment",
                fields=["experiment_id", "name"]
            )
        ]

    def __str__(self):
        return self.name


class InteractionManager(models.Manager):
    def record_conversion(self, access_token, experiment_id, participant_id):
        with connection.cursor() as cursor:
            return cursor.execute("""
            UPDATE hyp_interaction as i
            SET converted = TRUE
            FROM hyp_apikey as k
            WHERE k.customer_id = i.customer_id
            AND k.access_token = %s AND k.deactivated_at IS NULL
            AND i.experiment_id = %s AND i.participant_id = %s;
            """, [access_token, experiment_id, participant_id])


class Interaction(models.Model):
    objects = InteractionManager()

    id = models.BigAutoField(primary_key=True)
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
