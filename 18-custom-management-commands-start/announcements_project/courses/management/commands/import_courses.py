# this is going to import all of our courses.
# this is going to read a csv
# and create course instances
import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # this will be the help text if a user doesn't know how
    # what this command does.
    help = "Import courses from a CSV file"

    # we might be uploading various courses
    # add an argument for the path of the csv file.
    def add_argument(self, parser):
        parser.add_argument(
            "csv_file",  #
        )
