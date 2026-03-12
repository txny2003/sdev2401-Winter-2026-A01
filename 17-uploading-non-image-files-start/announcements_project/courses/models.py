from django.db import models
from django.conf import settings


# create an assignment model
class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignments"
    )

    def __str__(self):
        return self.title


# create a submission model
# - assignment: foreign key (use cascade)
# - student: name
# - file: filefield (upload to "submissions/")
# - subitted_at: DateTimeField when its' created.
class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    student_name = models.CharField(max_length=100)

    file = models.FileField(upload_to="submissions/")
    # inside of media this will uplaod to "submissions/"
    # we need to confirm we have the MEDIA_ROOT and MEDIA_URL

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission by {self.student_name} for {self.assignment}"
