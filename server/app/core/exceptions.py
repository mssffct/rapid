class NoEncryptionKey(Exception):
    def __str__(self):
        return "No encryption key found"
