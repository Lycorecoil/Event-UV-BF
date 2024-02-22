from django.contrib import admin
from .models import Event,Topic,Message

# Register your models here.
admin.site.register(Event)
admin.site.register(Topic)
admin.site.register(Message)