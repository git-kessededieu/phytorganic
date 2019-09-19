from django.db.models.signals import post_save
from django.dispatch import receiver

from frontend.models import Product


@receiver(post_save, sender = Product)
def add_reference(sender, instance, created, **kwargs):
    if created and sender == Product:
        initials = ''.join([x[0].upper() for x in instance.name.split(' ')])
        instance.reference = "#PRD{0}/{1}/{2}".format(initials, instance.created_at.date().strftime('%y%m%d'), instance.id)
        instance.save()

        pass
# instance.set_password(instance.password)
