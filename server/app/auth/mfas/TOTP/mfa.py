from fastapi_localization import lazy_gettext as _

from app.core.auth.mfa import BaseMFA


class TOTPMfa(BaseMFA):
    path = "app/auth/mfas/TOTP/"
    module_name = _("TOTP-based mfa")
    module_type = "TOTPMfa"
    module_desc = _("Time-based One-Time Password Multi-Factor Authentication")
