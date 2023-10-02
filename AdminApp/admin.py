from django.contrib import admin
from .models import UserProfile, Donate, Wastage,OTP,Track,PickupTeamUserProfile,distributionteamProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Wastage)
admin.site.register(Donate)
admin.site.register(Track)
admin.site.register(OTP)
admin.site.register(PickupTeamUserProfile)
admin.site.register(distributionteamProfile)