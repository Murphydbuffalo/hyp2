from allauth.account.signals import user_signed_up
from hyp.models import Customer
from django.dispatch import receiver
from django.contrib.auth.models import Group


@receiver(user_signed_up)
def create_customer(sender, request, user, **kwargs):
    customer = Customer(name=f"{user.email}'s team")
    customer.save()

    user.customer = customer
    user.save()

    team_admins = Group.objects.get(name="Team admins")
    user.groups.add(team_admins)
