# docs here: https://docs.djangoproject.com/en/5.2/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
from django.contrib.auth.mixins import UserPassesTestMixin


# we're goign to create a class that we can import rather than
# user the user_passes_test decorator.
class IsTeacherRoleMixin(UserPassesTestMixin):
    # we're creating our own role based auth test.

    # from the docs we need to specify the "test_func"
    def test_func(self):
        # the request will be on self.
        return self.request.user.role == "teacher"


# this is going to provide similar function to
# the decorator
# user_passes_test(is_teacher, login_url="login")
# where is_teacher is the test_func
