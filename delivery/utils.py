from .models import DeliveryAgentProfile, DeliveryAssignment
from django.db import transaction
from random import shuffle

def auto_assign_agent_to_order(order):
    available_profiles = list(DeliveryAgentProfile.objects.filter(
        agent__is_active=True,
        agent__is_delivery=True
    ).exclude(
        agent__delivery_assignments__status__in=['assigned', 'picked_up']
    ).distinct())

    shuffle(available_profiles)

    for profile in available_profiles:
        with transaction.atomic():
            DeliveryAssignment.objects.create(
                order=order,
                delivery_agent=profile.agent,
                status='assigned'
            )
            return profile.agent

    return None
