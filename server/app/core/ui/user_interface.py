from app.core.utils.images import image_to_base64


class UserInterface:
    @staticmethod
    def get_icons(path: str, default: str | None = None) -> dict[str, str]:
        default_icon_path = "app/core/icons/"
        try:
            return {
                "black": image_to_base64(f"{path}icon_black.png"),
                "white": image_to_base64(f"{path}icon_white.png"),
            }
        except Exception:
            return {
                "black": image_to_base64(
                    f"{default or default_icon_path}icon_black.png"
                ),
                "white": image_to_base64(
                    f"{default or default_icon_path}icon_white.png"
                ),
            }
