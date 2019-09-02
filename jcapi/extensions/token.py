from itsdangerous import URLSafeTimedSerializer
from itsdangerous import BadSignature
import hashlib


class TokenManager(object):

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app=None):
        self.secret_key = app.config['SECRET_KEY']
        self.security_password_salt = app.config['SECURITY_PASSWORD_SALT']
        self.serializer = URLSafeTimedSerializer(
            self.secret_key,
            salt=self.security_password_salt,
            signer_kwargs=dict(
                key_derivation='hmac',
                digest_method=hashlib.sha256)
        )

    def get_token(self, user_json):
        return self.serializer.dumps(user_json)

    def confirm_token(self, token, expiration=3600):
        try:
            data = self.serializer.loads(
                token,
                salt=self.security_password_salt,
                max_age=expiration
            )
        except BadSignature:
            return False
        return data
