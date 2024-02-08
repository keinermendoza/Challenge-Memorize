import csv
from django.db import transaction
from django.contrib import admin
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

class GetDataFromCSVForm(forms.Form):
    csv = forms.FileField()

    def clean_csv(self):
        csv = self.cleaned_data.get("csv")
        extension = csv.name.split(".")[-1].lower()

        if extension != "csv":
            raise forms.ValidationError("Só se permiten arquivos con extensão: csv")
        return csv


class CustomAdmin(admin.ModelAdmin):
    """
    Improve the functionality of uploading data via .csv
    """

    change_list_template = "admin/customs/change_list.html"

    def get_urls(self):
        """
        Add the url of the upload_csv view to the admin urls
        """

        urls = super().get_urls()
        new_urls = [path("upload-csv/", self.upload_csv)]

        return new_urls + urls

    def upload_csv(self, request):
        """
        Handle the upload of .csv files

        GET: Shows the form to upload the .csv file

        POST: Reads the .csv file and saves the data to the database
        """

        if request.method == "GET":
            form = GetDataFromCSVForm()

        elif request.method == "POST":
            form = GetDataFromCSVForm(request.POST, request.FILES)

            if form.is_valid():
                # Read the .csv file
                csv_file = form.cleaned_data["csv"]
                data_array_by_rows = csv_file.read().decode("utf-8").splitlines()
                csv_reader = csv.DictReader(data_array_by_rows)

                # Using a transaction to save all data as a single transaction, so if an error occurs, all previous processes are rolled back
                try:
                    with transaction.atomic():
                        for dict_obj in csv_reader:
                            # If the model is User, we create a user using the create_user method for password hashing
                            if self.model == User:
                                User.objects.create_user(**dict_obj)
                            else:
                                self.model.objects.create(**dict_obj)

                # Show error message when the .csv file is not in the correct format
                except Exception as e:
                    messages.warning(
                        request,
                        "It wasn't possible to proccess your request, please check the format of your file",
                    )
                    messages.error(request, f"{e}")
                    return redirect(request.path_info)
                else:
                    # Show success message when the data is saved successfully
                    messages.success(
                        request, "Your data was scceffully loaded!"
                    )
                    changelist_url = reverse(
                        "admin:%s_%s_changelist"
                        % (self.model._meta.app_label, self.model._meta.model_name)
                    )
                    return redirect(changelist_url)

        context = {"model_name": self.model.__name__, "form": form}

        return render(request, "admin/csv_upload.html", context)
