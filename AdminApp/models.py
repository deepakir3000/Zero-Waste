from django.contrib.auth.models import User
from django.db import models
import random
from django.core import validators
from django.core.exceptions import ValidationError
# Create your models here.

class UserProfile(models.Model):
    
    USER_TYPES = [
        ('Doner', 'Doner'),
        ('staff', 'staff'),
        
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='userdetails')
    profilePicture = models.ImageField(blank=True, null=True)
    DOB = models.DateField()
    address = models.TextField()
    contact_No = models.IntegerField()
    userType = models.CharField(
        max_length=10, choices=USER_TYPES, default='Doner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.user.username

class Wastage(models.Model):
    WASTE_TYPES = [
        ('Food', 'Food'),
        ('Cloth', 'Cloth'),
    ]
    STATUS_TYPES = [
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected','rejected'),
        ('Pickedup','Pickedup'),
        ('assignteam','assignteam'),
        ('donated','donated')
    ]
    donatedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    wasteType = models.CharField(
        max_length=10, choices=WASTE_TYPES, default='Food')
    statusType = models.CharField(
        max_length=10, choices=STATUS_TYPES, default='pending')
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    pic1 = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return f'Donated {self.wasteType} by {self.donatedBy.first_name}'
class Donate(models.Model):
    wastage= models.ForeignKey(Wastage, on_delete=models.SET_NULL, null=True)
    donated_to = models.CharField(max_length=255)
    donated_amount = models.PositiveIntegerField()
    address= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class OTP(models.Model):
    def otpgen():
        return str(random.randint(1000,9999))
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.SmallIntegerField(default=otpgen)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Tracking(models.Model):
    STATUS_TYPES = [
        ('PickedUp', 'PickedUp'),
        ('On the way', 'On the way'),
        ('Delivered', 'Delivered'),
    ]
    wastage = models.ForeignKey(Wastage, on_delete=models.SET_NULL, null=True)
    donate = models.ForeignKey(Donate, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_TYPES, default='PickedUp')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
class Track(models.Model):
    STATUS_TYPES = [
        ('Order Confirmed', 'Order Confirmed'),
        ('Picked by courier', 'Picked by courier'),
        ('On the way', 'On the way'),
        ('Ready for pickup', 'Ready for pickup'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    def TrackingIdGen():
       return str(random.randint(10000000, 99999999))
    track = models.ForeignKey(Wastage, on_delete=models.CASCADE)
    tracking_id=models.BigIntegerField(default=TrackingIdGen)
    shipped_by = models.CharField(max_length=255)
    delivery_by_name = models.CharField(max_length=255, null=True, blank=True)
    current_location = models.CharField(max_length=255)
    delivery_by_phn_no = models.PositiveIntegerField(null=True, blank=True)
    current_status = models.CharField(
        max_length=50, choices=STATUS_TYPES, default='Order Confirmed')
    cancelled_reason = models.CharField(max_length=255, null=True, blank=True)
    cancelled_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PickupTeamUserProfile(models.Model):
    def idgen():
       return str(random.randint(10000000,99999999))
    wastage=models.ForeignKey(Wastage,on_delete=models.CASCADE)
    pickup_boy_id=models.BigIntegerField(default=idgen)
    name=models.CharField(max_length=50)
    Date = models.DateField()
    address = models.TextField()
    contact_No = models.IntegerField()
    e_mail=models.EmailField()
    pass1=models.CharField(max_length=50)
    pass2=models.CharField(max_length=50)
    USER_TYPES = [
        ('Doner', 'Doner'),
        ('staff', 'staff'),
        
    ]
    userType = models.CharField(
        max_length=10, choices=USER_TYPES, default='Doner')
    TYPES = [
        ('a', 'a'),
        ('b', 'b'),
        
    ]
    Type = models.CharField(
        max_length=10, choices=TYPES, default='a')
    created_at = models.DateTimeField(auto_now_add=True)
    #action=models.CharField(max_length=100,null=True)

class distributionteamProfile(models.Model):
    def idgen():
       return str(random.randint(10000000,99999999))
    wastage=models.ForeignKey(Wastage,on_delete=models.CASCADE)
    pickup_boy_id=models.BigIntegerField(default=idgen)
    name=models.CharField(max_length=50)
    Date = models.DateField()
    address = models.TextField()
    contact_No = models.IntegerField()
    e_mail=models.EmailField()
    pass1=models.CharField(max_length=50)
    pass2=models.CharField(max_length=50)
    USER_TYPES = [
        ('Doner', 'Doner'),
        ('staff', 'staff'),
        
    ]
    userType = models.CharField(
        max_length=10, choices=USER_TYPES, default='Doner')
    TYPES = [
        ('a', 'a'),
        ('b', 'b'),
        
    ]
    Type = models.CharField(
        max_length=10, choices=TYPES, default='a')
    created_at = models.DateTimeField(auto_now_add=True)
