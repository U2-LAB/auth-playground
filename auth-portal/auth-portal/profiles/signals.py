from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from profiles.models import MyApplication

@receiver(pre_save, sender=MyApplication)
def delete_revoke_and_access_tokens(sender, instance, **kwargs):
    """Delete all tokens that belong to this app after changing scope"""
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        pass # Object is new, so field hasn't technically changed
    else:
        if not obj.scope == instance.scope: # Field has changed
            refresh_tokens = obj.refreshtoken_set.all()
            for token in refresh_tokens:
                token.revoke()
                token.delete()
