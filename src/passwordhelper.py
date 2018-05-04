import hashlib
import os
import base64


class PasswordHelper:
    """Password helpers"""

    @staticmethod
    def get_hash(text):
        return hashlib.sha512(text).hexdigest()

    @staticmethod
    def get_salt():
        return base64.b64encode(os.urandom(20)).decode('utf-8')

    def validate_password(self, password, salt, expected_hash):
        return self.get_hash((salt + password).encode('utf-8')) == expected_hash
