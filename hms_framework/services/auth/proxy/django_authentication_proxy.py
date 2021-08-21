from hms_framework.interfaces.auth.authentication_service import AuthenticationService
from django.contrib.auth import authenticate


class DjangoAuthenticationProxy(AuthenticationService):

    def is_a_valid_user(self, username, password) -> bool:
        user = authenticate(username=username, password=password)
        is_a_valid_user = user is not None
        return is_a_valid_user
