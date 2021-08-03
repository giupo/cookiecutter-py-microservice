"""
Auth module
"""

import os
import functools

from logging import getLogger

from jose import jwt
from jose.exceptions import JWTError


log = getLogger("{{cookiecutter.project_slug}}.auth")
DEFAULT_SECRET_DONT_USE_IN_PRODUCTION="secret" + ("0" * 16) ## change me


def verify_auth(token):
  try:
    secret = os.environ.get("SECRET", DEFAULT_SECRET_DONT_USE_IN_PRODUCTION)
    jwt.decode(token, secret, algorithms=['HS256'])
    return True
  except JWTError as e:
    return False

def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
      log.debug("checking authorization")
      token = self.get_cookie("jwt")
      token = "" if token is None else token
      if not verify_auth(token):
        log.debug("Faling auth with token: %s", token)
        self.set_status(403)
        self.finish({
          "status": 403,
          "message": "Not authenticated"
        })
      else:
        return method(self, *args, **kwargs)
    return wrapper
