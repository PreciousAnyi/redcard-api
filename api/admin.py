from django.contrib import admin
from .models import Card, RedCard, Exam, Blacklist

admin.site.register(Card)
admin.site.register(RedCard)
admin.site.register(Exam)
admin.site.register(Blacklist)