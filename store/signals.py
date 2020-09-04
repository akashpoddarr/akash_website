from django.db.models.signals import post_save,pre_save
from .models import Post, Customer
from django.contrib.auth.models import User
from django.dispatch import receiver, Signal


def save_post(sender, instance, **kwargs):
	print("Post save working")

def save_pre(sender, instance, **kwargs):
	print("pre save working")

post_save.connect(save_post, sender=Post)
pre_save.connect(save_pre, sender=Post)


@receiver(post_save, sender=User)
def profile_created(sender,instance,created, **kwargs):
    if created:
        Customer.objects.create(user=instance)