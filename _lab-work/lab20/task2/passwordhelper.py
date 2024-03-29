import hashlib, os, base64


class PasswordHelper:
    def get_hash(self, plain):
        return hashlib.sha512(plain).hexdigest()

    def get_salt(self):
        return base64.b64encode(os.urandom(20))

    def validate_password(self, plain, salt, expected):
        return self.get_hash((salt + plain).encode('utf-8')) == expected
