from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email","age",)
        
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields =  UserChangeForm.Meta.fields
        
        
# Or you can do what is below for both fields:
# ---> fields = ("username","email","age",)