from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    first_name = forms.CharField()
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField()

    phone_number = forms.CharField()

    address = forms.CharField(
        widget=forms.Textarea
    )

    country = forms.CharField()
    state = forms.CharField()
    city = forms.CharField()
    postal_code = forms.CharField()

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )

    account_type = forms.ChoiceField(
        choices=[
            ("Savings", "Savings Account"),
            ("Checking", "Checking Account"),
            ("Business", "Business Account"),
        ]
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "middle_name",
            "last_name",
            "phone_number",
            "address",
            "country",
            "state",
            "city",
            "postal_code",
            "date_of_birth",
            "account_type",
        ]