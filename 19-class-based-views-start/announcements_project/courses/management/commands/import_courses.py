import csv
from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand):
    help = 'Import courses from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import courses from')

    def handle(self, *args, **kwargs):
        csv_file = kwargs.get('csv_file')
        if not csv_file:
            self.stdout.write(self.style.ERROR('Please provide a CSV file path'))
            return

        number_of_created_courses = 0
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                course, created = Course.objects.get_or_create(
                    title=row['title'],
                    description=row['description']
                )
                if created:
                    number_of_created_courses += 1

        self.stdout.write(
            self.style.SUCCESS(
                F'Successfully created {number_of_created_courses} courses from {csv_file}'
            )
        )