from django import forms


# create a form that will take a single file
# and will validate that it's the correct file type.
class BulkAssignmentUploadForm(forms.Form):
    # single form file as the input
    csv_file = forms.FileField(
        label="Select a CSV file",
    )

    # validate the csv_file

    def clean_csv_file(self):
        # we're goign to get the csv data
        file = self.cleaned_data.get("csv_file")
        # check that the file ending is correct (.csv)
        # we can do this by checking file.name
        if not file.name.endswith(".csv"):
            raise forms.ValidationError(
                "Please Upload a CSV file",
            )

        # check that the content type is correct as well.
        if file.content_type != "text/csv":
            raise forms.ValidationError("File Type not a csv")

        # success
        return file
