from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

class Hash():
    def bcrypt(self, password: str):
        return pwd_context.hash(password)
