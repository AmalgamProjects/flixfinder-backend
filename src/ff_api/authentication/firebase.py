"""
https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication

Custom Authentication class to handle Firebase Authentication tokens.

We are delegating authentication to Firebase and so we'll be willing to
 accept any valid token as a valid user.

"""

import firebase_admin
import hashlib
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext_lazy as _

from firebase_admin import \
    auth as firebase_auth, \
    credentials as firebase_credentials

from rest_framework import \
    authentication, \
    exceptions

# Init Firebase
if settings.FIREBASE_KEY_FILE is not None:
    firebase_app = firebase_admin.initialize_app(
        firebase_credentials.Certificate(settings.FIREBASE_KEY_FILE)
    )


class FirebaseAuthentication(authentication.BaseAuthentication):
    """
    Firebase JWT based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Bearer ".  For example:

        Authorization: Bearer 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Bearer'

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            id_token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        if settings.FIREBASE_KEY_FILE is None:
            raise ImproperlyConfigured('No firebase key file.')

        import pprint

        """
        decoded_token = 
        {'aud': 'flixfinder-develop',
         'auth_time': 1589408123,
         'email': 'astrolox@gmail.com',
         'email_verified': True,
         'exp': 1589411723,
         'firebase': {'identities': {'email': ['astrolox@gmail.com'],
                                     'google.com': ['109016561945876411725']},
                      'sign_in_provider': 'google.com'},
         'iat': 1589408123,
         'iss': 'https://securetoken.google.com/flixfinder-develop',
         'name': 'Brian Wojtczak',
         'picture': 'https://lh3.googleusercontent.com/a-/AOh14Ggv_5N5org3n6Qpi7zfsCF3ETqpPy_xx-KxmeDgjQ',
         'sub': 'Hgo0ht7BKreAzMKyXEoGRl9WtNT2',
         'uid': 'Hgo0ht7BKreAzMKyXEoGRl9WtNT2',
         'user_id': 'Hgo0ht7BKreAzMKyXEoGRl9WtNT2'}
         """

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            pprint.pprint(decoded_token)
        except Exception as exception:
            msg = _('Invalid token.')
            raise exceptions.AuthenticationFailed(msg) from exception

        if not id_token or not decoded_token:
            msg = _('Invalid token.')
            raise exceptions.AuthenticationFailed(msg)

        # noinspection PyUnresolvedReferences
        try:
            user = User.objects.get(username=decoded_token.get('uid'))
        except User.DoesNotExist as exception:
            user = User.objects.create_user(
                username=decoded_token.get('uid'),
                email=decoded_token.get('email'),
                password=self.random_password(decoded_token.get('email'))
            )

        if not user.is_active:
            msg = _('User inactive or deleted.')
            raise exceptions.AuthenticationFailed(msg)

        return user, None

    def random_password(self, email):
        email = str(str(email) + str(uuid.uuid4())).strip().lower()
        bytes = email.encode()
        hash = hashlib.md5(bytes).hexdigest()
        return '%s' % hash

    def authenticate_header(self, request):
        return 'Firebase'
