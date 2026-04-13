# IMPORTANT these permissions should be in probably a core folder
# where the authentication/custom user would lie.
# because you want to share them across apps.

# we're going to use this permission and override it.
from rest_framework.permissions import BasePermission


# in this permission we're going to say if a user is trying to modify a workout log
# it should only be that user.
class IsOwnerOfResourceOrReadOnly(BasePermission):
    """
    Custom permission to allow owners of an object to edit it.
    This assumes that a model has a `user` attribute.
    """

    # this returns a boolean whether they have permission or not.
    # in an apiview check_object_permission needs to be called for this to be run.
    def has_object_permission(self, request, view, obj):
        breakpoint()
        # Read permissions on any request.
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True

        # if it hits this area you can see that's it's a PUT/POST/PATCH request
        # that will be modifying the items.
        return obj.user == request.user
        # Note 1: object is used from detail that will be passed in (ensure "user" is on the model)
        # Note 2: remember that the request.user will be the user based on the token that was
        # passed in the header

    # we're not defining this but below is run on every request.
    # def has_permission(self, request, view):
    #     return super().has_permission(request, view)
