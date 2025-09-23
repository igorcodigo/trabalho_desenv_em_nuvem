from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from apps.email_service.email_utils import send_welcome_email, send_email_changed_notification, send_password_changed_email

# Normalizar nome de usuário para minúsculas
@receiver(pre_save, sender=User)
def normalize_username(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()

CustomUser = get_user_model()

@receiver(pre_save, sender=CustomUser)
def store_old_data(sender, instance, **kwargs):
    """
    Store old data on the instance before it's saved.
    """
    print(f"--- PRE_SAVE signal for {instance.username} ---")
    if instance.pk:
        try:
            old_instance = CustomUser.objects.get(pk=instance.pk)
            instance._old_email = old_instance.email
            instance._old_password_hash = old_instance.password
            print(f"Storing old email: {instance._old_email}")
            print(f"Storing old password hash.")
        except CustomUser.DoesNotExist:
            instance._old_email = None
            instance._old_password_hash = None
            print("User does not exist yet, old data is None.")
    else:
        instance._old_email = None
        instance._old_password_hash = None
        print("New user, old data is None.")

@receiver(post_save, sender=CustomUser)
def user_post_save_receiver(sender, instance, created, **kwargs):
    """
    Handles sending emails to users on creation or update.
    """
    print(f"\n--- POST_SAVE signal for {instance.username} ---")
    
    name_to_send = instance.full_name or instance.username

    if created:
        print("User CREATED.")
        if instance.email:
            print(f"Sending welcome email to {instance.email}...")
            send_welcome_email(email=instance.email, name=name_to_send)
            print("Welcome email sent.")
    else:
        print("User UPDATED.")
        # Check for email change
        old_email = getattr(instance, '_old_email', None)
        print(f"Old email: {old_email}, New email: {instance.email}")
        if old_email != instance.email and instance.email:
            print(f"Email has changed. Sending notification to {instance.email}...")
            send_email_changed_notification(email=instance.email, name=name_to_send)
            print("Email changed notification sent.")
        else:
            print("Email has not changed.")

        # Check for password change
        old_password_hash = getattr(instance, '_old_password_hash', None)
        if old_password_hash != instance.password and instance.email:
            print(f"Password has changed. Sending notification to {instance.email}...")
            send_password_changed_email(email=instance.email, name=name_to_send)
            print("Password change notification sent.")
        else:
            print("Password has not changed.")
