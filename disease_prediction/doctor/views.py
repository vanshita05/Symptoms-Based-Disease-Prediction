from django.contrib import auth
from django.shortcuts import render, redirect
from user.models import *
from operator import attrgetter
# Create your views here.


def index(request):
    user = request.user.id
    u = Doctor.objects.get(user=user)
    logged_in_doctor = Doctor.objects.get(user=request.user)
    reviews = rating_review.objects.filter(doctor=logged_in_doctor)
    return render(request, 'doctor/index.html', {'u':u, 'reviews':reviews})


def profile(request):
    user = request.user.id
    u = Doctor.objects.get(user=user)
    return render(request, 'doctor/profile.html', {'u':u})


def edit_profile(request):
    pass
    user = request.user.id
    u = Doctor.objects.get(user=user)

    if request.POST:
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        gender = request.POST['gender']
        mobile_no = request.POST['mobile_no']
        img = request.FILES.get('img')
        registration_no = request.POST['registration_no']
        qualification = request.POST['qualification']
        specialization = request.POST['specialization']

        uid = Doctor.objects.get(user=user)
        uid.user.username = username
        uid.name = name
        uid.user.email = email
        uid.gender = gender
        uid.mobile_no = mobile_no
        uid.registration_no = registration_no
        uid.qualification = qualification
        uid.specialization = specialization

        if dob:
            uid.dob = dob

        if img:
            uid.img = img

        uid.user.save()
        uid.save()
        return redirect('/doctor/profile')
    return render(request, 'doctor/edit_profile.html', {'u':u})


def consultation_history(request):
    user = request.user.id
    u = Doctor.objects.get(user=user)

    if request.method == 'GET':
        doctorname = u.user.username
        duser = User.objects.get(username=doctorname)
        doctor_obj = duser.doctor
        consultation_doctor = consultation.objects.filter(doctor=doctor_obj)

        return render(request, 'doctor/consultation_history.html', {"consultation": consultation_doctor, "u":u})


def system_feedback(request):
    user = request.user.id
    u = Doctor.objects.get(user=user)
    if request.method == "POST":

        feedback = request.POST.get('feedback', None)
        if feedback != '':
            f = Feedback(sender=request.user, feedback=feedback)
            f.save()
            print(feedback)
            return redirect('/doctor/index')

    return render(request, 'doctor/system_feedback.html', {'u':u})


def signout(request):
    auth.logout(request)
    return render(request, 'user/index.html')

def consultationview(request, consultation_id):
    user = request.user.id
    u = Doctor.objects.get(user=user)
    user = request.user
    doctor = Doctor.objects.get(user=user)
    x = doctor.user
    if request.method == 'GET':
        request.session['consultation_id'] = consultation_id
        consultation_obj = consultation.objects.get(id=consultation_id)
        c = Chat.objects.filter(consultation_id=consultation_id, sender=x)
        other_user_msgs = Chat.objects.filter(consultation_id=consultation_id).exclude(sender=x)
        all_messages = Chat.objects.filter(consultation_id=consultation_id)
        all_messages = sorted(all_messages, key=attrgetter('created'))
        context = {
            'consultation_obj': consultation_obj,
            'u': u,
            'msg': c,
            'other_user_msgs': other_user_msgs,
            'all_messages': all_messages,
            'x': x
        }
        return render(request, 'doctor/chat.html', context)


def chat(request):
    user = request.user.id
    u = Doctor.objects.get(user=user)
    if request.method == "POST":
        msg = request.POST['chat-msg']
        consultation_id = request.session['consultation_id']
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj, sender=request.user, message=msg)

        if msg != '':
            c.save()
            print("msg saved" + msg)
            return redirect('/doctor/chat_messages')
        else:
            return HttpResponse('Request must be POST.')

    return render(request, 'doctor/chat.html',{'u':u})


def chat_messages(request):
    user = request.user.id
    u = Doctor.objects.get(user=user)
    user = request.user
    doctor = Doctor.objects.get(user=user)
    x = doctor.user
    if request.method == "GET":
         consultation_id = request.session['consultation_id']
         c = Chat.objects.filter(consultation_id=consultation_id, sender=x)
         other_user_msgs = Chat.objects.filter(consultation_id=consultation_id).exclude(sender=x)
         consultation_obj = consultation.objects.get(id=consultation_id)
         all_messages = Chat.objects.filter(consultation_id=consultation_id)
         all_messages = sorted(all_messages, key=attrgetter('created'))

         context = {
             'msg': c,
             'u': u,
             'other_user_msgs': other_user_msgs,
             'consultation_obj': consultation_obj,
             'all_messages': all_messages,
             'x': x
         }

         return render(request, 'doctor/chat.html', context)