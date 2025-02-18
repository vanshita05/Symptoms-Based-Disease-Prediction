from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from user.models import *
from user.models import consultation as Consultation
from django.contrib import messages
# Create your views here.

def index(request):
    user = request.user.id
    u = Madmin.objects.get(user=user)
    total_users = Usermodel.objects.count()
    total_doctor = Doctor.objects.count()
    total_consult = Consultation.objects.count()
    uid = Usermodel.objects.all().order_by('-pk')[:5]
    did = Doctor.objects.all().order_by('-pk')[:5]
    context = {
        'u': u,
        'total_users': total_users,
        'total_doctor':total_doctor,
        'total_consult':total_consult,
        'uid': uid,
        'did':did
    }
    return render(request, 'madmin/index.html', context)

def profile(request):
    user = request.user.id
    u = Madmin.objects.get(user=user)
    return render(request, 'madmin/profile.html',{'u':u})

def edit_profile(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)

    if request.POST:
        name = request.POST['name']
        dob = request.POST['dob']
        gender = request.POST['gender']
        mobile_no = request.POST['mobile_no']
        img = request.FILES.get('img')

        uid = Madmin.objects.get(user=user)
        uid.name = name
        uid.gender = gender
        uid.mobile_no = mobile_no

        if dob:
            uid.dob = dob

        if img:
            uid.img = img

        uid.save()
        return redirect('/madmin/profile')

    return render(request, 'madmin/edit_profile.html',{'u':u})



def signout(request):
    auth.logout(request)
    # request.session.pop('Usermodelid', None)
    return render(request, 'user/index.html')



def doctors(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)
    did = Doctor.objects.all()
    context = {
        'did': did,
        'u':u
    }
    return render(request, 'madmin/doctors.html', context)

def add_doctor(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)
    context = {
        'u': u
    }

    if request.method == 'POST':

        if request.POST['username'] and request.POST['email'] and request.POST['name'] and request.POST['dob'] and \
                request.POST['gender'] and request.POST['mobile_no'] and request.FILES['img'] and request.POST[
            'password'] and request.POST['password1'] and request.POST['registration_no'] and request.POST['qualification'] and \
                request.POST['specialization']:

            username = request.POST['username']
            email = request.POST['email']

            name = request.POST['name']
            dob = request.POST['dob']
            gender = request.POST['gender']
            mobile_no = request.POST['mobile_no']
            img = request.FILES['img']
            registration_no = request.POST['registration_no']
            qualification = request.POST['qualification']
            specialization = request.POST['specialization']

            password = request.POST.get('password')
            password1 = request.POST.get('password1')

            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'username already taken')
                    return redirect('/madmin/add_doctor')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email already taken')
                    return redirect('/madmin/add_doctor')

                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()

                    doctornew = Doctor(user=user, name=name, dob=dob, gender=gender, img=img,
                                       mobile_no=mobile_no, registration_no=registration_no,
                                     qualification=qualification, specialization=specialization)
                    doctornew.save()
                    messages.info(request, 'user created sucessfully')

                return redirect('/madmin/doctors')

            else:
                messages.info(request, 'password not matching, please try again')
                return redirect('/madmin/add_doctor')

        else:
            messages.info(request, 'Please make sure all required fields are filled out correctly')
            return redirect('/madmin/add_doctor')

    return render(request, 'madmin/add_doctor.html',context)

def edit_doctor(request,id):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)

    # doctor_id = request.GET.get(id=id)
    doctor = Doctor.objects.get(pk=id)
    # user = User.objects.get(username=username)
    # doctor = Doctor.objects.get(user=user)

    context = {
        'u': u,
        'doctor': doctor
    }

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
        password = request.POST['password']


        doctor.user.username = username
        doctor.name = name
        doctor.user.email = email
        if dob:
            doctor.dob = dob
        doctor.gender = gender
        doctor.mobile_no = mobile_no
        if img:
            doctor.img = img
        doctor.registration_no = registration_no
        doctor.qualification = qualification
        doctor.specialization = specialization
        doctor.password = password

        doctor.user.save()
        doctor.save()

        return redirect('/madmin/doctors')

    return render(request, 'madmin/edit_doctor.html', context)

def doctor_profile(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)

    doctor_id = request.GET.get('id')
    doctor = Doctor.objects.get(pk=doctor_id)
    context = {
        'u': u,
        'doctor': doctor
    }
    return render(request, 'madmin/doctor_profile.html',context)


def delete_doctor(request,id):
    did = Doctor.objects.get(pk=id)
    # u = uid.user.id
    did.delete()
    return redirect('/madmin/doctors')


def users(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)
    uid = Usermodel.objects.all()
    context = {
        'uid': uid,
        'u':u
    }
    return render(request, 'madmin/users.html', context)

def add_user(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)
    context = {
        'u': u
    }

    if request.method == 'POST':

        if request.POST['username'] and request.POST['email'] and request.POST['name'] and request.POST['dob'] and request.POST['gender'] and request.POST['mobile_no'] and request.FILES['img'] and request.POST['password'] and request.POST['password1']:

            username = request.POST['username']
            email = request.POST['email']

            name = request.POST['name']
            dob = request.POST['dob']
            gender = request.POST['gender']
            mobile_no = request.POST['mobile_no']
            img = request.FILES['img']
            password = request.POST.get('password')
            password1 = request.POST.get('password1')

            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'username already taken')
                    return redirect('/madmin/add_user')

                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'email already taken')
                    return redirect('/madmin/add_user')

                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.save()

                    usernew = Usermodel(user=user, name=name, dob=dob, gender=gender, img=img,
                                         mobile_no=mobile_no)
                    usernew.save()
                    messages.info(request, 'user created sucessfully')

                return redirect('/madmin/users')

            else:
                messages.info(request, 'password not matching, please try again')
                return redirect('/madmin/add_user')

        else:
            messages.info(request, 'Please make sure all required fields are filled out correctly')
            return redirect('/madmin/add_user')

    return render(request, 'madmin/add_user.html', context)

def edit_user(request,id):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)

    uid = Usermodel.objects.get(pk=id)
    context = {
        'u': u,
        'uid': uid
    }

    if request.POST:
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        gender = request.POST['gender']
        mobile_no = request.POST['mobile_no']
        img = request.FILES.get('img')
        password = request.POST['password']

        uid.user.username = username
        uid.name = name
        uid.user.email = email
        if dob:
            uid.dob = dob
        uid.gender = gender
        uid.mobile_no = mobile_no
        if img:
            uid.img = img
        uid.password = password

        uid.user.save()
        uid.save()

        return redirect('/madmin/users')


    return render(request, 'madmin/edit_user.html', context)

def user_profile(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)

    user_id = request.GET.get('id')
    uid = Usermodel.objects.get(pk=user_id)
    context = {
        'u': u,
        'uid': uid
    }
    return render(request, 'madmin/user_profile.html', context)



def delete_user(request,id):
    uid = Usermodel.objects.get(pk=id)
    # u = uid.user.id
    uid.delete()
    return redirect('/madmin/users')


def consultation(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)
    context = {
        'u': u
    }
    return render(request, 'madmin/consultation.html', context)



def disease_info(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)

    did = Diseasescan.objects.all()
    context = {
        'u': u,
        'did': did,
    }
    return render(request, 'madmin/disease_info.html', context)


def system_feedback(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)
    fid = Feedback.objects.all()

    context = {
        'fid': fid,
        'u':u
    }
    return render(request, 'madmin/system_feedback.html', context)


def chat(request):
    pass
    user = request.user.id
    u = Madmin.objects.get(user=user)
    context = {
        'u': u
    }
    return render(request, 'madmin/chat.html', context)