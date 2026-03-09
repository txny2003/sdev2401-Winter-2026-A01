from django.core.management.base import BaseCommand
# import send_mail
from django.core.mail import send_mail

# import the Submission model
from courses.models import Submission


class Command(BaseCommand):
    help = 'Notify instructors about new submissions'

    def handle(self, *args, **kwargs):
        # Fetch submissions that have not been notified yet
        new_submissions = Submission.objects.filter(instructor_notified=False)

        # loop through submissions
        count = new_submissions.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No new submissions to notify instructors about.'))
            return

        for submission in new_submissions:
            instructor = submission.assignment.owner
            # Simulate sending notification (e.g., via email)
            send_mail(
                subject='New Submission Received',
                message=f'{submission.assignment.title} has a new submission from {submission.student_name}.',
                from_email="notifications@test.com",
                recipient_list=[instructor.email],
            )

            # Mark submission as notified
            submission.instructor_notified = True
            submission.save()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully notified instructors about {count} new submissions.'
            )
        )