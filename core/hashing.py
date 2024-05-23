from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hasher:
    """Class for passwords hashing."""

    @staticmethod
    def verify_password(plain_pass, hashed_pass):
        """Verify hashed and unhashed passwords."""
        return pwd_context.verify(plain_pass, hashed_pass)

    @staticmethod
    def get_hashed_password(password):
        """Hash password."""
        return pwd_context.hash(password)
