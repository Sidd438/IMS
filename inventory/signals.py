from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import ItemDepartmentMember

@receiver(post_save, sender=ItemDepartmentMember)
def update_issued_items(sender, instance, created, update_fields, **kwargs):
    if created:
        instance.Item.total_issued += int(instance.quantity)
        instance.Item.total_stock -= int(instance.quantity)
        instance.Item.save()