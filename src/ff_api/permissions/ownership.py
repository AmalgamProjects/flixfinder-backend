"""
Flix-finder

Authentication or identification by itself is not usually sufficient to gain access to information or code.
For that, the entity requesting access must have authorization.

http://www.django-rest-framework.org/api-guide/permissions/#permissions
"""

import logging

from rest_framework import permissions

# Get an instance of a logger
logger = logging.getLogger(__name__)


class IsOwner(permissions.IsAuthenticated):
    """
    Object-level permission to restrict access to a specific object to only it's owner.
    Assumes the model instance has an `user` attribute ...
     or has a `username` attribute which indicates that it is the user model
    """

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            obj_user = obj.user
        elif hasattr(obj, 'username'):
            obj_user = obj
        else:
            logger.warning('No user reference found on obj %s' % str(obj))
            return False
        # Is owner?
        return obj_user == request.user

