from django.core.mail import send_mail
from rest_framework import permissions


def send_activation_email(user):
    subject = 'Спасибо за регистрацию на нашем сайте.'
    body = 'Спасибо за регистрацию на нашем сайте.\n' \
           'Для активации перейдите по следующей ссылке:\n' \
           f'{user.activation_code}/'
    from_email = 'ek-makeup@django.kg'
    recipients = [user.email]
    send_mail(subject=subject,
              message=body,
              from_email=from_email,
              recipient_list=recipients,
              fail_silently=False)


class IsOwnerAccount(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or bool(request.user and request.user.is_superuser)
