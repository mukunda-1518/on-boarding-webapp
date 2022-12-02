from django.contrib.auth.models import User

from .models import CustomUser


class CommonMethods:

    def get_custom_user(self, username):
        user_obj = User.objects.get(username=username)
        custom_user_obj = CustomUser.objects.get(user=user_obj)
        return custom_user_obj
