

class CacheManager:

    def __init__(self):
        pass

    @staticmethod
    def manager() -> "CacheManager":
        return CacheManager()

    async def get(self, delete: bool = False):
        pass

    async def pop(self):
        return await self.get(delete=True)

