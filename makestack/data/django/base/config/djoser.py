from djoser import email, utils
from djoser.conf import settings
from django.contrib.auth.tokens import default_token_generator


class ActivationEmail(email.BaseEmailMessage):
    template_name = "activation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context


class ConfirmationEmail(email.BaseEmailMessage):
    template_name = "confirmation.html"


class PasswordResetEmail(email.BaseEmailMessage):
    template_name = "password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context
