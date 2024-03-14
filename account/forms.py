from django.contrib.auth.forms import UserCreationForm as DefaultUserCreationForm
from django.forms import modelform_factory, ModelForm
from .models import User

class UserCreationForm(DefaultUserCreationForm):
    class Meta(DefaultUserCreationForm.Meta):
        model = User
        fields = DefaultUserCreationForm.Meta.fields + ("profile_name",)

#modelform_factory(model=User, fields=["username", "profile_name", "email", "bio"], )

class UserInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        for k in self.Meta().fields:
            self.fields[k].required = False

    class Meta:
        model = User
        fields = ["profile_name", "email", "bio"]

    @staticmethod
    def formClassFromFieldsFactoryDict():
        fields = UserInfoForm.Meta().fields
        formclasses = {}
        for field in fields:
            formclasses[field] = modelform_factory(model=User, fields=[field])
        return formclasses
