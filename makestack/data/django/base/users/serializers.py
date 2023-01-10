from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as STokenPairSerializer,
)


class TokenObtainPairSerializer(STokenPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["first_name"] = user.first_name
        token["last_name"] = user.last_name

        return token
