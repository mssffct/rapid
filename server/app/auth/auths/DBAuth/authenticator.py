from fastapi_localization import lazy_gettext as _

from app.core.auth.authenticator import BaseAuthenticator


class DBAuth(BaseAuthenticator):
    path = "app/auth/auths/DBAuth/"
    module_name = _("Database Authenticator")
    module_type = "DBAuth"
    module_desc = _("Using database  to authenticate")

    external = False

    def authenticate(self):
        pass
