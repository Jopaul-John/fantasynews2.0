from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from itertools import chain
from fantasyapp.forms import *
from fantasyapp.models import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
import random,json
from django.core.mail import send_mail, BadHeaderError,EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.http import JsonResponse,HttpResponse

from social_django.models import UserSocialAuth

def returnuserprofile(user):
    user = UserProfile.objects.get(user=user)
    return user

def index(request):
    return HttpResponseRedirect('/home/')

def adminlogin(request):
    if request.user.is_superuser:
        return HttpResponseRedirect('/post/')

    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        message = "Successful login"
        if user:
            login(request,user)
            return HttpResponseRedirect('/post/')
        else:
            message = "Invalid Credentials"
            return render(request,'admin.html',{'message':message})
    else:
        return render(request,'admin.html',{})

def matchview():
    cricketma = Cricket.objects.all()
    footballma = Football.objects.all()
    for var in cricketma:
        match = Match()
        match.tournament = var.tournament
        match.match_name = var.cricket_match_name
        match.save()
    for var in footballma:
        match = Match()
        match.tournament = var.tournament
        match.match_name = var.football_match_name
        match.save()
    return
def post(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home/')
    tournament_foot = Tournament.objects.filter(is_football=True)
    tournament_cric = Tournament.objects.filter(is_cricket=True)
    print(tournament_cric)
    print(tournament_foot)
    if request.POST:
        cricform = cricketform(request.POST,request.FILES)
        footform = footballform(request.POST,request.FILES)
        message = "error"
        if cricform.is_valid():
            cricform.updated_on = datetime.now()
            cric = cricform.save()
            match = Match()
            match.tournament = cric.tournament
            match.match_name = cric.cricket_match_name
            match.save()
            message = "succesfully posted"
        elif footform.is_valid():
            footform.updated_on = datetime.now()
            foot = footform.save()
            match = Match()
            match.tournament = foot.tournament
            match.match_name = foot.football_match_name
            match.save()
            print("inside football")
            message = "succesfully posted"
        return render(request, 'adminpost.html', {'message': cricform.errors or footballform.errors})

    return render(request,'adminpost.html',{'foot':tournament_foot,'cric':tournament_cric})


def home(request):
    #matchview()
    cricmatch = Cricket.objects.all().order_by('-id')[:8]
    footmatch = Football.objects.all().order_by('-id')[:8]
    match = sorted(chain(cricmatch, footmatch),key=lambda instance: instance.on_date,reverse=True)[:8]
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = request.POST.get('redirecturl')
        print(url)
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            if url:
                return HttpResponseRedirect(url)
            else:
                return render(request, 'home.html', {'match': match,'active':True,'user':user,})
        else:
            message = "Invalid credentials"
            return render(request, 'home.html', {'match':match,'msg':message} )
    else:
        if request.user.is_authenticated:
            return render(request, 'home.html', {'match': match, 'active': True, 'user': request.user})

    return render(request,'home.html',{'match':match})

def userpage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    else:
        return render(request,'user.html',{'active':True})


def cricket(request):
    tournament = Tournament.objects.filter(is_cricket=True,is_active=True)
    cricket_matches = Cricket.objects.all().order_by('-id')
    return render(request, 'cricket.html', {'cricket': cricket_matches,'tournament':tournament})

def cricket_matches(request,id):
    try:
        user = returnuserprofile(request.user)
    except:
        user = None
    if request.user.is_authenticated :
        active = True
    else:
        active = False
    match_info = Cricket.objects.get(id=id)
    discussions = FAQ.objects.filter(match__match_name=match_info.cricket_match_name)
    if request.POST:
        if not request.user.is_authenticated or not user.is_active:
            return JsonResponse({'message':"False"})
        else:
            print("else")
            comment = request.POST.get('comment')
            match = Match.objects.get(match_name=match_info.cricket_match_name)
            faqob = FAQ()
            print(faqob.id)
            faqob.match = match
            faqob.user= returnuserprofile(request.user)
            faqob.comment=comment
            faqob.save()
            #discussions = FAQ.objects.filter(match__match_name=match_info.cricket_match_name)
            data = {'comment': comment,
                    'user': format(request.user)
                    }
            print("before f]json")
            return JsonResponse(data)
    return render(request,'cricketmatch.html',{'cric':match_info,'discuss':discussions,'url':False,'active':active})


def crictournament(request,id):
    mytournament = Tournament.objects.filter(is_cricket=True,is_active=True)
    tournament = Tournament.objects.get(id=id)
    cricket_match = Cricket.objects.filter(tournament=tournament)
    return render(request,'cricket.html',{'cricket': cricket_match,'tournament':mytournament})

def foottournament(request,id):
    mytournament = Tournament.objects.filter(is_football=True,is_active=True)
    tournament = Tournament.objects.get(id=id)
    football_match = Football.objects.filter(tournament=tournament)
    return render(request,'football.html',{'football': football_match,'tournament':mytournament})


def football_match(request,id):
    try:
        user = returnuserprofile(request.user)
    except:
        user = None
    if request.user.is_authenticated:
        active = True
    else:
        active = False
    match_info = Football.objects.get(id=id)

    discussions = FAQ.objects.filter(match__match_name=match_info.football_match_name)
    if request.POST:
        if not request.user.is_authenticated or not user.is_active:
            print("indide not aunthenticated")
            return JsonResponse({'message':"False"})
        else:

            comment = request.POST.get('comment')
            print("snknaskdnkajb"+format(comment))
            match = Match.objects.get(match_name=match_info.football_match_name)
            faqob = FAQ()
            faqob.match = match
            faqob.user = returnuserprofile(request.user)
            faqob.comment = comment
            faqob.save()
            #discussions = FAQ.objects.filter(match__match_name=match_info.football_match_name)
            data = {'comment':comment,
                    'user':format(request.user)
                    }
            print("before f]json")
            return JsonResponse(data)
    else:
        return render(request,'footballmatch.html',{'foot':match_info,'discuss':discussions,'url':False,'active':active})

def football(request):
    tournament = Tournament.objects.filter(is_football=True,is_active=True)
    football_matches = Football.objects.all().order_by('-id')
    return render(request, 'football.html', {'football': football_matches,'tournament':tournament})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home/')

def settings(request):
    try:
        user = UserProfile.objects.get(user=request.user)
    except:
        user = UserProfile()
        user.user = request.user
        user.email = request.user.email
        user.is_active = True
        user.credits = 0
        user.save()
    return HttpResponseRedirect('/home/')

def register(request):
    if request.POST:
        userformset = userform(request.POST)
        profileformset = userprofileform(request.POST)
        user =None
        message=None
        if userformset.is_valid():
            user = userformset.save()
            user.set_password(user.password)
            user.save()

        else:
            message = userformset.errors
        if profileformset.is_valid():
            profile = profileformset.save(commit=False)
            profile.user = user
            profile.activation_code = random.randint(100000,999999)
            profile.save()
            user = User.objects.get(username=user)
            user.email =profile.email
            user.save()
            if user:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request,user)
            else:
                return HttpResponse("error adichu in login in register")
            subject = "Hello "+format(user.username)+ " Thank You for being the part of fantasynews family :)"
            message = "127.0.0.1:8000/activate/"+format(user.username)+'/'+format(profile.activation_code)
            sendmail(user,subject,message)
            message = "we have send a verification link to your mail id.Kindly verify your account"
        else:
            message = profileformset.errors
        return render(request,'register.html',{'msg':message})
    else:
        return render(request,'register.html',{})

def activate(request,linkuser,id):
    if not request.user.is_authenticated:
        return HttpResponse('You have to login')
    user = returnuserprofile(request.user)
    print(user.activation_code)
    print(id)
    if format(user.activation_code) == format(id) and format(linkuser) == format(request.user):
        if not user.is_active:
            user.is_active = True
            user.save()
            return HttpResponse("account activated")
        else:
            return HttpResponse("already active")
    else:
        return HttpResponse("Invalid verification Link")

def sendmail(user,subject,message):
    html = get_template('email.html')

    try:
        toaddress=[user.email]
    except:
        toaddress = [user]

    username = Context({'user':user})
    print(username)
    htmlcontent = html.render({'username':username,'message':message})
    emaildetail = EmailMultiAlternatives(subject,message,'scrappyteam.in@gmail.com',toaddress)
    print("after email detail")

    emaildetail.attach_alternative(htmlcontent,'text/html')
    try:
        print("inside send mail try")
        emaildetail.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')

def credits(request):
    try:
        user = UserProfile.objects.get(user=request.user)
        user.credits = user.credits + 15
        user.save()
    except:
        pass
    return JsonResponse({'yeah':"yeah"})


def contact(request):
    print(request.user)
    if request.POST:
        name = format(request.POST.get('name'))
        place = format(request.POST.get('place'))
        mobile = format(request.POST.get('mobile'))
        message = format(request.POST.get('msg'))
        email = format(request.POST.get('email'))
        print(name+place+mobile+email+message)
        contact = ContactUs()
        contact.Name = name
        contact.place = place
        contact.mobile = mobile
        contact.message = message
        contact.email = email
        flag = 0
        try:
            print(contact)
            message ={'message': "your question is sucessfully posted "}
            contactmessage = "Thank you for giving your feedback for us..We will be in touch with you as soon as possible.\n Meanwhile if you have noy registered in fantasynews register today itself :)"
            subject = "Fantasy News -Thank you for giving your feedback"
            sendmail(email,subject,contactmessage)
            print("inside contacy try")
            contact.save()
            return JsonResponse(message)
        except:
            message ={'message': "Please enter a valid email "}
            return JsonResponse(message)

def adminmail(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home/')
    contact_msg = ContactUs.objects.filter(status=True)
    if request.POST:
        answer = format(request.POST.get('message'))
        print("answer = "+answer)
        id = format(request.POST.get('id'))
        try:
            reply_msg = ContactUs.objects.get(id=id)
            message = answer
            subject = "regarding you enquiry about "+format(reply_msg.message)
            sendmail(format(reply_msg.email),subject,message)
            reply_msg.status = False
            reply_msg.reply = answer
            reply_msg.save()
            print(answer+id)
            status = {'status':"yes"}
            return JsonResponse(status)
        except:
            status = {'status': "no"}
            return JsonResponse(status)
    return render(request,'adminmail.html',{'messages':contact_msg})