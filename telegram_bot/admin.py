from django.contrib import admin
from .models import Telebot_Users

import decimal, csv
from django.http import HttpResponse
from django.db.models import F


# Register your models here.

def export_books(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="books.csv"'
    writer = csv.writer(response)
    writer.writerow(['teleUser_mobilenum', 'teleUser_name', 'teleUser_familyname', 'teleUser_edu', 'teleUser_field', 'teleUser_place', 'teleuser_dateadded'])
    books = queryset.values_list('Name', 'Family_Name', 'Mobile_Number', 'Education', 'Field', 'Location', 'Date_Added')
    for book in books:
        writer.writerow(book)
    return response
export_books.short_description = 'Export to csv'


class telebotAdmin(admin.ModelAdmin):
    list_display = ('Mobile_Number', 'Name', 'Date_Added', 'Status')
    actions= [export_books]

admin.site.register(Telebot_Users, telebotAdmin)