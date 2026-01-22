import abc


from app.core.ui import UserInterface
from app.core.schemas.type_responses import TypeWithImageResponse


class BaseModule(UserInterface, abc.ABC):
    """
    Base class for all modules
    """

    is_base: bool = True
    path: str = "app/core"

    module_name: str = "Base module"
    module_type: str = "BaseModule"
    module_desc: str = "Base module description"

    def get_type_info(self):
        return TypeWithImageResponse(
            type=self.module_type,
            name=self.module_name,
            desc=self.module_desc,
            icons=self.get_icons(self.path),
        )
