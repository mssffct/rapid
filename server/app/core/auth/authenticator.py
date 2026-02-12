from app.core.module import BaseModule


class BaseAuthenticator(BaseModule):
    mfa_enabled = False

    def __init__(self):
        super().__init__(self)
