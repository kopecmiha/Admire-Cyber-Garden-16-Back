from rest_framework_jwt.serializers import jwt_payload_handler
import jwt
from main import settings


def get_jwt_token(user):
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return token