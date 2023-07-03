from templated_mail.mail import BaseEmailMessage


class ActivationEmail(BaseEmailMessage):
    template_name = "activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["code"] = user.verify_code
        return context


class ConfirmationEmail(BaseEmailMessage):
    template_name = "confirmation.html"

    pass


class PasswordRecoveryEmail(BaseEmailMessage):
    template_name = "password_recovery.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["password"] = user.stash
        return context
