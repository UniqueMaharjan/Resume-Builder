from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(ResumeUser)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Projects)
admin.site.register(Skills)
admin.site.register(Interests)