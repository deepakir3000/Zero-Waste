from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile,Wastage,OTP,Track,PickupTeamUserProfile,distributionteamProfile
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def Auth_Register_View(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        DOB = request.POST.get('DOB')
        profile_pic = request.FILES.get('pic')
        address = request.POST.get('address')
        userType=request.POST.get('userType')

        if pass1 != pass2:
            message = 'Password should be same !'
            return render(request, 'auth-register.html', {'message': message})
        if contact.isdigit():
            s=str(contact)
            t=s.split()
            c=0
            for x in t:
                for i in x:
                    c=c+1
            if c!=10:
                message = 'number must be 10 digits'
                return render(request, 'auth-register.html', {'message': message})
        if not email.endswith('@gmail.com'):
            message = 'incorrect email format'
            return render(request, 'auth-register.html', {'message': message})

        try:
            u = User.objects.create_user(
                username=username, email=email, password=pass1, first_name=first_name, last_name=last_name)
        except:
            message = 'User name already exists!'
            return render(request, 'auth-register.html', {'message': message})

        UserProfile.objects.create(
            user=u, contact_No=contact, DOB=DOB, profilePicture=profile_pic, address=address,userType=userType)

        return redirect('admin-login')

    return render(request, 'auth-register.html')

def Auth_Login_View(request):
    return render(request, 'auth-login.html')

def index_view(request):
    if not request.user.is_authenticated:
        return render(request,'auth-login.html')
    donate=Wastage.objects.filter(donatedBy=request.user).count()
    approvewaste=Wastage.objects.filter(donatedBy=request.user).filter(statusType='approved').count()
    pendingwaste=Wastage.objects.filter(donatedBy=request.user).filter(statusType='pending').count()
    return render(request,'index.html',context={'total_donate':donate,'approvewaste':approvewaste,"pendingwaste":pendingwaste})


def Login(request):
    msg=''
    if request.method == "POST":
        user = request.POST["username"]
        password = request.POST["password"]
        data = authenticate(username=user, password=password)
        if data != None:
            login(request, data)
            if data.is_superuser:
                return redirect("indexadmin")
            if data.userdetails.userType=='staff':
                return redirect("indexadmin")
            if data.userdetails.userType=='Doner':
                return redirect("public-index")
            
           


        msg='Incorrect username or password'
        return render(request, 'auth-login.html',{'msg':msg})
    return render(request, 'auth-login.html',{'msg':msg})
     

def Logout(request):
    logout(request)
    return redirect("public-index")

def CollectFood(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        pic1 = request.FILES.get('pic1')

        wastage = Wastage.objects.create(
            donatedBy=request.user,wasteType='Food', description=description, quantity=quantity, pic1=pic1)

        return redirect('admin-index')

    return render(request,'wastagefood.html')

def CollectCloth(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        username = request.user.username
        #wasteType= request.POST.get('wasteType')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        pic1 = request.FILES.get('pic1')

        wastage = Wastage.objects.create(
            donatedBy=request.user,wasteType='Cloth', description=description, quantity=quantity, pic1=pic1)

        return redirect('admin-index')

    return render(request, 'wastagetypecloth.html')

def ChangePassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    message = ''
    if request.method == 'POST':
        oldpass = request.POST.get('oldpass')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            message = 'Password should be same !'
            return render(request, 'changepassworduser.html', {'message': message})
        try:
            u = User.objects.get(username=request.user.username)
        except:
            message = 'Please enter correct User Name!'
            return render(request, 'changepassworduser.html', {'message': message})

        check = u.check_password(oldpass)
        if check:
            u.set_password(pass1)
            u.save()
            data = authenticate(username=u.username, password=pass1)
            if data != None:
                login(request, data)
                return redirect("admin-index")
        message = 'Please enter valid Old password!'
        return render(request, 'changepassworduser.html', {'message': message})
    return render(request, 'changepassworduser.html')


def ForgotPassword(request):
    message = ''
    if request.method == 'POST':
        otp=request.POST.get('otp')
        uname = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 != pass2:
            message = 'Password should be same !'
            return render(request, 'auth-forgot-password.html', {'message': message})
        try:
            u = User.objects.get(username=uname) 
        except:
            message = 'Please enter correct User Name!'
            return render(request, 'auth-forgot-password.html', {'message': message})
        try:
            Otp=OTP.objects.filter(user=u).order_by('-created_at').first()
        except:
            message = 'invalid otp!'
            return render(request, 'auth-forgot-password.html', {'message': message}) 
        #print(type(otp)) 
        #print(type(Otp.otp))
        if Otp.otp==int(otp):
            u.set_password(pass1)
            u.save()
            return redirect('login')
    return render(request, 'auth-forgot-password.html')


def UserProfileUser(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'userprofileuser.html')


def UserProfileAdmin(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'userprofileadmin.html')

def ChangePhotoAdmin(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        photo = request.FILES.get('file')
        u = UserProfile.objects.get(user=request.user)
        u.profilePicture = photo
        u.save()
        return redirect("userprofileadmin")


def ChangePhotoUser(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'POST':
        photo = request.FILES.get('file')
        u = UserProfile.objects.get(user=request.user)
        u.profilePicture = photo
        u.save()
        return redirect("userprofile")

def indexadminview(request):
    if not request.user.is_authenticated:
        return render(request,'auth-login.html')
    donate=Wastage.objects.filter(donatedBy=request.user).count()
    approvewaste=Wastage.objects.filter(donatedBy=request.user).filter(statusType='approved').count()
    pendingwaste=Wastage.objects.filter(donatedBy=request.user).filter(statusType='pending').count()
    return render(request,'indexadmin.html',context={'total_donate':donate,"approvewaste":approvewaste,"pendingwaste":pendingwaste})
   
def pickupview(request):
    return render(request,'pickuptrack.html')
def trackwasteview(request):
    return render(request,'trackwaste.html')
def userapproval(request):
    status=Wastage.objects.filter(statusType='pending')
    return render(request,'userapproval.html',{'status':status})
def donatehistory(request):
    w=Wastage.objects.filter(donatedBy=request.user)
    return render(request,'donatehistory.html',{'w':w})
def track_view(request):
    wastage = Wastage.objects.filter(donatedBy=request.user).order_by('-created_at')
    return render(request, 'track.html', {'wastage':wastage})

def CreateTrack(request, id):
    waste = Wastage.objects.get(id=id)
    if request.method == 'POST':
        waste = Wastage.objects.get(id=id)
        shipped_by = request.POST.get('shipped_by')
        
        # breakpoint()
        t = Track(shipped_by=shipped_by,
                   track=waste)
        t.save()
        subject = 'Donation Approval'
        body = 'Your donation is approved. Thanks for donation. Team Zero Waste.'
        from_email = settings.EMAIL_HOST_USER
        to_email = [waste.donatedBy.email]
        waste.statusType = 'approved'
        waste.save()
        send_mail(subject, body, from_email, to_email)
        # return redirect(f'approvewaste/{waste.id}')
        wastage = Wastage.objects.all().order_by('-created_at')
        Dict = {'wastage': wastage}
        return render(request, 'track.html', Dict)
    return render(request, 'trackwaste.html', {'waste': waste})

def TrackingId(request,id):
    waste = Wastage.objects.get(id=id)
    # assign = PickupTeamUserProfile.objects.get(id=id)
    # print(assign)
    Dict = {'Trackid': waste}
    if waste.statusType == 'approved':
        return render(request, 'trackingid.html', Dict)
    return render(request, 'pickuptrack.html', Dict)

def Assignpickupteam(request,id):
    waste = Wastage.objects.get(id=id)
    if request.method=='POST':
        waste = Wastage.objects.get(id=id)
        #waste.statusType='assignteam'
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        name=request.POST.get('username')
        pickup_boy_id=request.POST.get('id')
        address=request.POST.get('address')
        date=request.POST.get('date')
        contact=request.POST.get('contact')
        mail = request.POST.get('mail')
        profile_pic = request.FILES.get('pic')
        userType=request.POST.get('userType')
        if pass1 != pass2:
           return render(request,'assignforpickup.html',{'waste':waste})
        if contact.isdigit():
            s=str(contact)
            t=s.split()
            c=0
            for x in t:
                for i in x:
                    c=c+1
            if c!=10:
                
                return render(request,'assignforpickup.html',{'waste':waste})
        if not mail.endswith('@gmail.com'):
           return render(request,'assignforpickup.html',{'waste':waste})
        
        p=PickupTeamUserProfile.objects.create(wastage=waste,pickup_boy_id=pickup_boy_id,name=name,Date=date,address=address,contact_No=contact,e_mail=mail,pass1=pass1,pass2=pass2)
        try:
            u=User.objects.get(username=name)
        except User.DoesNotExist:
            u=User.objects.create_user(username=name, email=mail, password=pass1)
        try:
            UserProfile.objects.get(user=u)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=u, contact_No=contact, profilePicture=profile_pic, address=address,userType=userType,DOB=date)
        waste.statusType ='assignteam'
        waste.save()
        subject = 'Donation ready for pick'
        body = f'Hello {waste.donatedBy}, Your waste is {waste.id} is ready for pickup'
        from_email = settings.EMAIL_HOST_USER
        to_email = [waste.donatedBy.email]
        send_mail(subject, body, from_email, to_email)
        subject = 'Assign for pickup'
        body = f'Hello {p.name}, You will assign for waste {waste.id}  for pickup and your username={p.name} and password={p.pass1}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [p.e_mail]
        send_mail(subject, body, from_email, to_email)

        return redirect('pickupteamprofile')
    return render(request,'assignforpickup.html',{'waste':waste})

def distributionteam(request,id):
    waste = Wastage.objects.get(id=id)
    if request.method=='POST':
        waste = Wastage.objects.get(id=id)
        #waste.statusType='assignteam'
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        name=request.POST.get('username')
        pickup_boy_id=request.POST.get('id')
        address=request.POST.get('address')
        date=request.POST.get('date')
        contact=request.POST.get('contact')
        mail = request.POST.get('mail')
        profile_pic = request.FILES.get('pic')
        userType=request.POST.get('userType')
        if pass1 != pass2:
           return render(request,'assignforpickup.html',{'waste':waste})
        if contact.isdigit():
            s=str(contact)
            t=s.split()
            c=0
            for x in t:
                for i in x:
                    c=c+1
            if c!=10:
                
                return render(request,'assignforpickup.html',{'waste':waste})
        if not mail.endswith('@gmail.com'):
           return render(request,'assignforpickup.html',{'waste':waste})
        
        p=distributionteamProfile.objects.create(wastage=waste,pickup_boy_id=pickup_boy_id,name=name,Date=date,address=address,contact_No=contact,e_mail=mail,pass1=pass1,pass2=pass2)
        try:
            u=User.objects.get(username=name)
        except User.DoesNotExist:
            u=User.objects.create_user(username=name, email=mail, password=pass1)
        try:
            UserProfile.objects.get(user=u)
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=u, contact_No=contact, profilePicture=profile_pic, address=address,userType=userType,DOB=date)
        waste.statusType ='donated'
        waste.save()
        subject = 'Donation ready for pick'
        body = f'Hello {waste.donatedBy}, Your waste is {waste.id} is ready for distribute'
        from_email = settings.EMAIL_HOST_USER
        to_email = [waste.donatedBy.email]
        send_mail(subject, body, from_email, to_email)
        subject = 'Assign for pickup'
        body = f'Hello {p.name}, You will assign for waste {waste.description}  for distribution and your username={p.name} and password={p.pass1}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [p.e_mail]
        send_mail(subject, body, from_email, to_email)
        return redirect('distributionteam')
    return render(request, 'adddistributionteam.html',{'waste': waste})


def Rejectwaste(request,id):
    w=Wastage.objects.get(id=id)
    w.statusType='Rejected'
    w.save()
    subject = 'Waste management team'
    body = f'Hello {request.user.username}, Your wastage is rejected'
    from_email = settings.EMAIL_HOST_USER
    to_email=[w.donatedBy.email]
    send_mail(subject, body, from_email,to_email)
    return redirect('userapproval')

def OTPverify(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            u = User.objects.get(username=username)
        except:
            message = 'Please enter valid Username !'
            return render(request, 'otpverification.html', {'message': message})
        try:
            email = u.email
        except:
            message = 'Invalid Email !'
            return render(request, 'otpverification.html', {'message': message})
        subject = 'OTP for Waste Management User'
        otp = OTP.objects.create(user=u)
        body = f'Hello {u.username}, Your OTP is {otp.otp}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        send_mail(subject, body, from_email, to_email)
        return redirect('forgotpassword')
    return render(request, 'otpverification.html')

def pickupteamprofile(request):
    pickupemp=Wastage.objects.filter(statusType='approved')
    # for x in pickupemp:
    #     print(x.wastage.description)
    return render(request,'pickupteam.html',{"pickupemp":pickupemp})

def assigndistribution(request):
    pickupemp=Wastage.objects.filter(statusType='Pickedup')
    return render(request,'assigndistrib.html',{"pickupemp":pickupemp})

def addpickupboy(request):
    if request.method=="POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        date = request.POST.get('date')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        mail = request.POST.get('mail')
        if contact.isdigit():
            s=str(contact)
            t=s.split()
            c=0
            for x in t:
                for i in x:
                    c=c+1
            if c!=10:
                
                return render(request,'addpickupboy.html')
        if not mail.endswith('@gmail.com'):
           return render(request,'addpickupboy.html')
        PickupTeamUserProfile.objects.create(wastage=waste,pickup_boy_id=id,name=name,Date=date,address=address,contact_No=contact,email=mail)
        return redirect("pickupteamprofile")
    return render(request,'addpickupboy.html')

def Allusers(request):
    all=UserProfile.objects.all()
    return render(request,'allusers.html',{"all":all})

def UserDetails(request, id):
    detail = UserProfile.objects.get(id=id)
    if request.method == 'POST':
        photo = request.FILES.get('file')
        u = UserProfile.objects.get(id=id)
        u.profilePicture = photo
        u.save()
        details = UserProfile.objects.get(user=u.user)
        return render(request, 'userdetails.html',{'details': detail})
    
    
    return render(request, 'userdetails.html',{'details': detail})

def editpickupboy(request,id):
    w=Wastage.objects.get(id=id)
    if request.method=='POST':
        donatedBy=request.POST.get('donatedby')
        quantity=request.POST.get('quantity')
        wasteType=request.POST.get('wasteType')
        w=Wastage.objects.get(id=id)
        w.donatedBy=donatedBy
        w.quantity=quantity
        w.wasteType=wasteType
        w.save()
        return redirect('pickupteamprofile')
    return render(request,'editwastage.html',{'w':w})

def editdistributionteam(request,id):
    w=Wastage.objects.get(id=id)
    if request.method=='POST':
        donatedBy=request.POST.get('donatedby')
        quantity=request.POST.get('quantity')
        wasteType=request.POST.get('wasteType')
        w=Wastage.objects.get(id=id)
        w.donatedBy=donatedBy
        w.quantity=quantity
        w.wasteType=wasteType
        w.save()
        return redirect('assigndistribteam')
    return render(request,'editdistribteam.html',{'w':w})

def deletepickupboy(request,id):
    w=Wastage.objects.get(id=id)
    w.delete()
    return redirect('showpickteam')

def deletedistributionteam(request,id):
     w=Wastage.objects.get(id=id)
     w.delete()
     return redirect('assigndistribteam')


def edituser(request,id):
    detail = UserProfile.objects.get(id=id)
    if request.method=='POST':
        username=request.POST.get('name')
        email = request.POST.get('email')
        contact1 = request.POST.get('contact')
        userType = request.POST.get('userType')
        profile_pic1 = request.FILES.get('pic')
        address1= request.POST.get('address')
        if contact1.isdigit():
            s=str(contact1)
            t=s.split()
            c=0
            for x in t:
                for i in x:
                    c=c+1
            if c!=10:
                
                return render(request, 'edituser.html',{'details': detail})
        if not email.endswith('@gmail.com'):
           return render(request, 'edituser.html',{'details': detail})
        u=UserProfile.objects.get(id=id)
        u.user.username=username
        u.user.email_address=email
        u.contact_No=contact1
        u.address=address1
        u.profilePicture=profile_pic1
        u.userType=userType
        u.save()
        return redirect('alluser')
    return render(request, 'edituser.html',{'details': detail})

def showpickteam(request):
    pickupemp=PickupTeamUserProfile.objects.all()
    return render(request,'showpickteam.html',{"pickupemp":pickupemp})

def editpickup(request,id):
    detail =PickupTeamUserProfile.objects.get(id=id)
    if request.method=='POST':
        waste = Wastage.objects.get(id=id)
        name=request.POST.get('name')
        pickup_boy_id=request.POST.get('id')
        address=request.POST.get('address')
        date=request.POST.get('date')
        contact=request.POST.get('contact')
        if contact.isdigit():
            s=str(contact)
            t=s.split()
            c=0
            for x in t:
                for i in x:
                    c=c+1
            if c!=10:
                
                return render(request,'editpickup.html',{'details':detail})
        
        u=PickupTeamUserProfile.objects.get(id=id)
        #u.user=username
        #u.userdetails.Email=email
        u.name=name
        u.address=address
        u.Date=date
        u.contact_No=contact
        u.pickup_boy_id=pickup_boy_id
        u.save()
        return redirect('showpickteam')
    return render(request,'editpickup.html',{'details':detail})

def editdistribution(request,id):
    detail =distributionteamProfile.objects.get(id=id)
    if request.method=='POST':
        waste = Wastage.objects.get(id=id)
        name=request.POST.get('name')
        pickup_boy_id=request.POST.get('id')
        address=request.POST.get('address')
        date=request.POST.get('date')
        contact=request.POST.get('contact')
        if contact.isdigit():
            s=str(contact)
            t=s.split()
            c=0
            for x in t:
                for i in x:
                    c=c+1
            if c!=10:
                
                return render(request, 'editdistribution team.html',{'details': detail})
        
        u=distributionteamProfile.objects.get(id=id)
        #u.user=username
        #u.userdetails.Email=email
        u.name=name
        u.address=address
        u.Date=date
        u.contact_No=contact
        u.pickup_boy_id=pickup_boy_id
        u.save()
        return redirect('distributionteam')
    return render(request, 'editdistribution team.html',{'details': detail})

def deletepickup(request,id):
    detail =PickupTeamUserProfile.objects.get(id=id)
    detail.delete()
    return redirect('pickupteamprofile')

def deletedistribution(request,id):
    detail =distributionteamProfile.objects.get(id=id)
    detail.delete()
    return redirect('distributionteam')

def distributionteamview(request):
    distribteam=distributionteamProfile.objects.all()
    return render(request,'distributionteam.html',{'distribteam':distribteam})

def adddistributionteam(request):
    if request.method=="POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        mail = request.POST.get('mail')
        wasteid = request.POST.get('wasteid')
        if contact.isdigit():
            s=str(contact)
            t=s.split()
            c=0
            for x in t:
                for i in x:
                    c=c+1
            if c!=10:
                
                return render(request,'adddistributionteam.html')
        if not mail.endswith('@gmail.com'):
           return render(request,'adddistributionteam.html')
        try:
            distributionteamProfile.objects.get(name=name)
        except distributionteamProfile.DoesNotExist:
            distributionteamProfile.objects.create(pickup_boy_id=id,name=name,address=address,contact_No=contact,e_mail=mail,waste_id=wasteid)
        return redirect("distributionteam")
    return render(request,'adddistributionteam.html')

def stockupdateview(request):
    wastage = Wastage.objects.filter(statusType='Pickedup')
    return render(request,'stockupdate.html',{'wastage':wastage})

def deletestock(request,id):
    wastage = Wastage.objects.get(id=id)
    wastage.statusType='pending'
    wastage.save()
    return redirect('stockupdate')

def addstockview(request):
    return render(request,'addstock.html')

def confirmview(request):
    waste=PickupTeamUserProfile.objects.filter(name=request.user).filter(Type='a')
    return render(request,'confirm.html',{'waste':waste})

def confirmdistributionview(request):
    waste= distributionteamProfile.objects.filter(name=request.user).filter(Type='a')
    return render(request,'confirm1.html',{'waste':waste})
    
def confirmpickup(request,id):
    waste=Wastage.objects.get(id=id)
    if request.method=='POST':
        waste=Wastage.objects.get(id=id)
        quantity = request.POST.get('quantity')
        pic1 = request.FILES.get('pic1')
        waste.pic1=pic1
        waste.statusType='Pickedup'
        waste.save()
        p=PickupTeamUserProfile.objects.get(wastage=id)
        p.Type='b'
        p.save()
        subject = 'Pickup Team'
        body = f'Hello {p.name}, Your wastage is pickedup.'
        from_email = {p.e_mail}
        to_email=[settings.EMAIL_HOST_USER]
        send_mail(subject, body, from_email,to_email)
        return redirect('pickupteamprofile')

    return render(request,'confirmpickup.html',{'waste':waste})

def confirmdistrib(request,id):
    waste=Wastage.objects.get(id=id)
    if request.method=='POST':
        waste=Wastage.objects.get(id=id)
        quantity = request.POST.get('quantity')
        pic1 = request.FILES.get('pic1')
        pic2 = request.FILES.get('pic2')
        waste.pic1=pic1
        waste.pic2=pic2
        waste.statusType='donated'
        waste.save()
        p=distributionteamProfile.objects.get(wastage=id)
        p.Type='b'
        p.save()
        subject = 'Distribution Team'
        body = f'Hello {p.name}, Your wastage is successfully donated'
        from_email = {p.e_mail}
        to_email=[settings.EMAIL_HOST_USER]
        send_mail(subject, body, from_email,to_email)
        return redirect('distributionteam')

    return render(request,'confirm3.html',{'waste':waste})