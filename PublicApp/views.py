from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from PublicApp.models import contact,feedback
# Create your views here.
def public_index_view(request):
    return render(request,'index1.html')

def public_about_view(request):
    return render(request,'about.html')
    
def public_contact_view(request):
    message1=''
    sent=False
    if request.method == "POST":
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        if name and message and subject and email:
            contact.objects.create(name=name,email=email,subject=subject,message=message)
            sent=True
            message1='Thanks for contact us, we will contact u very soon'
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            subject='Team zero waste'
            body='Thank u for contact us.We will contact u soon'
            send_mail(subject, body, from_email, to_email)
           
        
    return render(request,'contact1.html',{'message1':message1})
def public_service_view(request):
    return render(request,'service.html')

def public_feedback_view(request):
    feed=feedback.objects.all()
    if request.method == "POST":
        name=request.POST['name']
        email=request.POST['email']
        mobile=request.POST['mobile']
        feedback1=request.POST['feedback']
        if name and email and mobile and feedback:
            feedback.objects.create(name=name,mobile=mobile,email=email,feedback=feedback1)
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            subject='Team zero waste'
            body='Thank u for your feedback .'
            send_mail(subject, body, from_email, to_email)
        
    return render(request,'feedback.html',{'feed':feed})