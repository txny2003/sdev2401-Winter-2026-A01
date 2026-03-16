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
            "csv_file",  # arguemnt name
            type=str,  # this will be a string
            help="Path to file for import",
        )

    # *args and **kwargs, you'll see this a lot this means
    # args (which are positinal arguments) are a list in the
    # function
    # kwargs (named arguments) are a dictionary of named
    # items.
    # this makes it so that you can pass in a flexible
    # number of arguments.
    # Note: the function below is what will be executed
    def handle(self, *args, **kwargs):
        print("Hello from my command!")
