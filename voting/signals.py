from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from voting.models import Vote


@receiver(pre_save, sender=Vote)
def adjust_num_of_votes_of_menu(sender, instance: Vote, **kwargs):
    if instance.id is None:
        instance.menu.increment_num_of_votes()
    else:
        previous_instance = Vote.objects.get(id=instance.id)
        if instance.menu != previous_instance.menu:
            previous_instance.menu.decrement_num_of_votes()
            instance.menu.increment_num_of_votes()


@receiver(pre_delete, sender=Vote)
def decrement_num_of_votes_of_menu(sender, instance: Vote, **kwargs):
    instance.menu.decrement_num_of_votes()
