from fastapi_localization import lazy_gettext as _

from app.core.auth.authenticator import BaseAuthenticator


class IPAuth(BaseAuthenticator):
    path = "app/auth/auths/IPAuth/"
    module_name = _("IP Authenticator")
    module_type = "IPAuth"
    module_desc = _("Using IP to authenticate")
