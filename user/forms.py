from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from .models import Customer

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Customer

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password1"])  # Manually hash the password
        if commit:
            user.save()
        return user
