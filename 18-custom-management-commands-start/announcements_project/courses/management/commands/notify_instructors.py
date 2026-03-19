from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from courses.models import Submission


# to create a command
# with no arguments
class Command(BaseCommand):
    help = "Notifies instructors of new submissions"

    def handle(self, *args, **kwargs):
        # will get all submissions that the instructor
        # has not been notified.
        new_submissions = Submission.objects.filter(
            instructor_notified=False,
        )
        # count submissions
        count = new_submissions.count()
        # loop through the submissions
        for submission in new_submissions:
            to_email = submission.assignment.owner.email
            # send an email
            send_mail(
                subject=f"New submssion from {submission.student_name} for {submission.assignment.title}",
                message=f"""
                {submission.assignment.title} has a new submission from {submission.student_name}

                Download it here: {submission.file.url}
                """,
                from_email="notifications@do-not-reply.com",  # your admin email.
                recipient_list=[to_email],
            )
            # update each submission model
            # say that the instructor has been notified.
