from django.db import models
from uuid import uuid4


def create_access_token():
    return uuid4().hex


class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    models.Index(fields=["name"])

    def __str__(self):
        return self.name


class ApiKey(models.Model):
    access_token = models.UUIDField(default=create_access_token)
    name = models.CharField(max_length=200, unique=True)
    production = models.BooleanField(default=False)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)
    deleted_at = models.DateTimeField('deleted at', null=True, blank=True)
    last_used_at = models.DateTimeField('last used at', null=True, blank=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    models.UniqueConstraint(fields=["customer_id", "production"], name="One key per environment")

    def __str__(self):
        return f'{"PRODUCTION" if self.production else "SANDBOX"}/{self.access_token}'


class Experiment(models.Model):
    name = models.CharField(max_length=200)
    stopped = models.BooleanField(default=False)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    models.Index(fields=["name"])
    models.Index(fields=["stopped"])

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

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

    models.Index(fields=["experiment_id", "participant_id"])

    class Meta:
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
