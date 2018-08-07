from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to='avatar/'
    )


@receiver(post_delete, sender=Profile)
def avatar_delete(sender, instance, **kwargs):
    instance.file.delete(False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Post(models.Model):
    content = models.TextField(
        null=False,
        blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_post = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(
        null=False,
        blank=False,
        upload_to='upload/'
    )
    privacy = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)


@receiver(post_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
    instance.file.delete(False)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(
        null=False,
        blank=False
    )
    date_comment = models.DateTimeField(auto_now_add=True)
