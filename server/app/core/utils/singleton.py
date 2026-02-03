import typing


class Singleton(type):
    """
    Singleton pattern
    """
    _instance: typing.Optional[typing.Any]

    def __init__(cls: 'Singleton', *args: typing.Any, **kwargs: typing.Any) -> None:
        """
        Initialize the Singleton metaclass for each class that uses it
        """
        cls._instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls: 'Singleton', *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
