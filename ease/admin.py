from django.contrib import admin
from .models import UserModel, FMModel, TVModel, NotificationModel
# Register your models here.
admin.site.register(UserModel)
admin.site.register(FMModel)
admin.site.register(TVModel)
admin.site.register(NotificationModel)
