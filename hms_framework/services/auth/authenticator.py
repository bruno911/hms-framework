from hms_framework.interfaces.auth.authentication_service import AuthenticationService


class Authenticator:

    def __init__(self, authentication_service: AuthenticationService):
        self.authentication_service = authentication_service

    def is_a_valid_user(self, username, password):
        return self.authentication_service.is_a_valid_user(username, password)
