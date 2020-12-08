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

# TODO: Do we want to go even further and log an event for every API request?
# When it was made, what the IP was, what the API key was? Why? Slower, more
# code, less privacy for the user...
# You'd want that as an audit log, so users can review how their tokens are being
# used
#
# TODO: We probably want to associate tokens with users at some point.
# Right now a Customer is the only entity, but it seems likely customers will
# want separate logins and permissions for various users (eg user management,
# vs experiment management, vs only being able to manage a specific experiment
# vs having read-only access),
# and we'd need a user model to support that case. Maybe simplest to just go
# forward with only a Customer entity at this point?
# They should be able to revoke/cancel their tokens, and once we introduce
# role-based permissions we can use those to figure out what the API key associated
# with a user is allowed to do
# TODO: should we/how do we build off of Django's built-in user model from the
# auth module?
class ApiKey(models.Model):
    # TODO: make sure you're using these tokens in a secure way. They are an
    # authorization mechanism only, in the sense that the holder of the token
    # doesnt need to authenticate to use it. If they have it, we grant them access
    # SO, do some security best practices:
    # 1. Figure out how to encrypt this at rest in the DB
    # 2. Show them only one time the user
    # 3. Only communicate over TLS
    # 4. Should these auto-expire? Probably not...
    # But we can suggest via email that the user rotate them every 6 months or
    # so and make an easy UI/API for doing that
    # TODO: let's include SANDOX/PRODUCTION as part of the access token itself
    access_token = models.CharField(max_length=200, default=create_access_token)
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
        return f'Experiment {self.experiment_id}, Variant {self.variant_id}, Participant {self.participant_id}. Converted? {self.converted}'
