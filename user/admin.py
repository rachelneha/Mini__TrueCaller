from django.contrib import admin

from user.models import SpamNumber, Contact

admin.site.register(Contact)
admin.site.register(SpamNumber)
