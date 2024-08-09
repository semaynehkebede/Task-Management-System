# external import
import jwt
from rest_framework import permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from tms_back import settings
from .models import CUser

class CustomJWTAuthentication(BaseAuthentication):
    
    def authenticate(self, request):

        # Get the JWT token from the request headers
        # header = request.get_authorization_header(request).decode('utf-8')
        header = request.META.get('HTTP_AUTHORIZATION')
        # if not header:
        if not header:
            raise AuthenticationFailed('No credentials provided.')
        # check if the header is an instance of string(is header string) because split is done only in string
        if isinstance(header, str):
            # None represent whitespace, 1 represent the first whitespace
            header_components = header.split(None, 1)
        else:
            header_components = []
            
        if len(header_components) != 2 or header_components[0].lower() != 'bearer':
            raise AuthenticationFailed('Authorization header must be of the form "Bearer <token>".')
        
        token = header_components[1]
        return self.authenticate_token(token)
        

    def authenticate_token(self, token):
        try:
            # Decode the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        user_id = payload.get('user_id')
        if not user_id:
            raise AuthenticationFailed('Token payload is missing user_id.')

        try:
            user = CUser.objects.get(id=user_id)
        except CUser.DoesNotExist:
            raise AuthenticationFailed('User does not exist.')

        return (user, token)  # (user, token)

    # def authenticate_header(self, request):
    #     return 'Bearer'