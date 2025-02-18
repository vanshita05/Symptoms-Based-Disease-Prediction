from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import generate_token
from disease_prediction import settings
from .models import *

import torch
import torch.nn as nn
import numpy as np
from operator import attrgetter

from datetime import datetime


# Create your views here.


def index(request):
    return render(request, 'user/index.html')



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if auth.authenticate(username=username, password=password).is_superuser:

                user = auth.authenticate(username=username, password=password, is_superuser=True)
                if user is not None:
                    auth.login(request, user)
                    return redirect('/admin/')
            elif Madmin.objects.filter(user=user, is_admin=True):
                auth.login(request, user)
                return redirect('/madmin/index')

            elif Doctor.objects.filter(user=user, is_doctor=True):
                auth.login(request, user)

                return redirect('/doctor/index')

            elif Usermodel.objects.filter(user=user, is_user=True):
                auth.login(request, user)

                request.session['p_user_try'] = user.username
                return redirect('/user_panel')
            
            else:
                messages.error(request, "Bad Credentials")
                return redirect('login')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('login')

    return render(request, 'user/login.html')

def register(request):
    return render(request, 'user/register.html')

def doctor_register(request):
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
                    messages.error(request, 'username already taken')
                    return redirect('doctor_register')

                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'email already taken')
                    return redirect('doctor_register')

                else:
                    user = User.objects.create_user(username=username, password=password, email=email)
                    user.is_active = False
                    user.save()

                    doctornew = Doctor(user=user, name=name, dob=dob, gender=gender, img=img,
                                       mobile_no=mobile_no, registration_no=registration_no,
                                     qualification=qualification, specialization=specialization)
                    doctornew.save()
                    messages.success(request, 'user created sucessfully')

                    #Welcome Email

                    subject = "Welcome to DiseaseScan!"
                    message = "Hello " + doctornew.name + "!! \n \n" + "Welcome to DiseaseScan! \n \nThank you for registering with us and visiting our website. We are thrilled to have you as part of our community. To complete your registration and activate your account, please confirm your email address by clicking on the link sent to your email. \n \nIf you did not receive the confirmation email, please check your spam folder. \n \nShould you have any questions or need assistance, feel free to reach out to us at diseasescan@gmail.com. \n \nThank you for choosing DiseaseScan. We look forward to helping you manage your health better. \n \nBest regards, \nThe DiseaseScan Team"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

                    # Email Address Confirmation Email
                    current_site = get_current_site(request)
                    email_subject = "Activate your account and join to DiseaseScan!!"
                    message2 = render_to_string('email_confirmation.html', {

                        'name': doctornew.name,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': generate_token.make_token(user)
                    })
                    email = EmailMessage(
                        email_subject,
                        message2,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                    )
                    email.fail_silently = True
                    email.send()

                return redirect('login')

            else:
                messages.error(request, 'password not matching, please try again')
                return redirect('doctor_register')

        else:
            messages.error(request, 'Please make sure all required fields are filled out correctly')
            return redirect('doctor_register')
    else:
        return render(request, 'user/doctor_register.html')

def user_register(request):
    if request.method == 'POST':

        if request.POST['user_name'] and request.POST['email'] and request.POST['name'] and request.POST['dob'] and request.POST['gender'] and request.POST['mobile_no'] and request.FILES['img'] and request.POST['password'] and request.POST['password2']:

            user_name = request.POST['user_name']
            email = request.POST['email']

            name = request.POST['name']
            dob = request.POST['dob']
            gender = request.POST['gender']
            mobile_no = request.POST['mobile_no']
            img = request.FILES['img']
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                if User.objects.filter(username=user_name).exists():
                    messages.error(request, 'username already taken')
                    return redirect('user_register')

                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'email already taken')
                    return redirect('user_register')

                else:
                    user = User.objects.create_user(username=user_name, password=password, email=email)
                    user.is_active = False
                    user.save()

                    usernew = Usermodel(user=user, name=name, dob=dob, gender=gender, img=img,
                                         mobile_no=mobile_no)
                    usernew.save()
                    messages.error(request, 'user created sucessfully')


                    #Welcome Email

                    subject = "Welcome to DiseaseScan!"
                    message = "Hello " + usernew.name + "!! \n \n" + "Welcome to DiseaseScan! \n \nThank you for registering with us and visiting our website. We are thrilled to have you as part of our community. To complete your registration and activate your account, please confirm your email address by clicking on the link sent to your email. \n \nIf you did not receive the confirmation email, please check your spam folder. \n \nShould you have any questions or need assistance, feel free to reach out to us at diseasescan@gmail.com. \n \nThank you for choosing DiseaseScan. We look forward to helping you manage your health better. \n \nBest regards, \nThe DiseaseScan Team"
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

                    # Email Address Confirmation Email
                    current_site = get_current_site(request)
                    email_subject = "Activate your account and join to DiseaseScan!!"
                    message2 = render_to_string('email_confirmation.html', {

                        'name': usernew.name,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': generate_token.make_token(user)
                    })
                    email = EmailMessage(
                        email_subject,
                        message2,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                    )
                    email.fail_silently = True
                    email.send()


                return redirect('login')

            else:
                messages.error(request, 'password not matching, please try again')
                return redirect('user_register')

        else:
            messages.error(request, 'Please make sure all required fields are filled out correctly')
            return redirect('user_register')



    else:
        return render(request, 'user/user_register.html')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('login')
    else:
        return render(request,'activation_failed.html')


def signout(request):
    auth.logout(request)
    # request.session.pop('Usermodelid', None)
    return render(request, 'user/index.html')


def about(request):
    return render(request, 'user/about.html')

def doctors(request):
    return render(request, 'user/doctors.html')

def feedback(request):
    return render(request, 'user/feedback.html')


def profile(request):

    user = request.user.id
    u = Usermodel.objects.get(user=user)

    return render(request, 'user/profile.html', {'u':u})

def edit_profile(request):
    pass
    user = request.user.id
    u = Usermodel.objects.get(user=user)

    if request.POST:
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        gender = request.POST['gender']
        mobile_no = request.POST['mobile_no']
        img = request.FILES.get('img')

        uid = Usermodel.objects.get(user=user)
        uid.user.username = username
        uid.name = name
        uid.user.email = email
        uid.gender = gender
        uid.mobile_no = mobile_no

        if dob:
            uid.dob = dob

        if img:
            uid.img = img

        uid.user.save()
        uid.save()
        return redirect('profile')


    return render(request, 'user/edit_profile.html', {'u':u})



def user_panel(request):
    user = request.user.id
    u = Usermodel.objects.get(user=user)

    uid = Diseasescan.objects.filter(patient=u)

    return render(request, 'user/user_panel.html', {'u':u,'uid':uid})


def consultation_history(request):
    user = request.user.id
    u = Usermodel.objects.get(user=user)

    if request.method == 'GET':
        usern = u.user.username
        puser = User.objects.get(username=usern)
        user_obj = puser.usermodel
        consultation_user = consultation.objects.filter(patient = user_obj)

        context = {
            'u':u,
            'consultation':consultation_user
        }

        return render(request, 'user/consultation_history.html', context)

def system_feedback(request):
    user = request.user.id
    u = Usermodel.objects.get(user=user)
    if request.method == "POST":

        feedback = request.POST.get('feedback', None)
        if feedback != '':
            f = Feedback(sender=request.user, feedback=feedback)
            f.save()
            print(feedback)
            return redirect('user_panel')
    return render(request, 'user/system_feedback.html', {'u':u})



def disease_prediction(request):
    user = request.user.id
    u = Usermodel.objects.get(user=user)

    diseaselist = ['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer diseae',
                   'AIDS', 'Diabetes ',
                   'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine', 'Cervical spondylosis',
                   'Paralysis (brain hemorrhage)',
                   'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B',
                   'Hepatitis C', 'Hepatitis D',
                   'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
                   'Dimorphic hemmorhoids(piles)',
                   'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
                   'Osteoarthristis',
                   'Arthritis', '(vertigo) Paroymsal  Positional Vertigo', 'Acne', 'Urinary tract infection',
                   'Psoriasis', 'Impetigo']

    symptomslist = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                    'joint_pain',
                    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
                    'spotting_ urination',
                    'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
                    'restlessness', 'lethargy',
                    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes',
                    'breathlessness', 'sweating',
                    'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
                    'loss_of_appetite', 'pain_behind_the_eyes',
                    'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine',
                    'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
                    'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation',
                    'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                    'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                    'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                    'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                    'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                    'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints',
                    'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                    'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                    'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
                    'belly_pain',
                    'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes', 'increased_appetite',
                    'polyuria', 'family_history', 'mucoid_sputum',
                    'rusty_sputum', 'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                    'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                    'history_of_alcohol_consumption', 'fluid_overload', 'blood_in_sputum', 'prominent_veins_on_calf',
                    'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring', 'skin_peeling',
                    'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
                    'red_sore_around_nose',
                    'yellow_crust_ooze']

    alphabaticsymptomslist = sorted(symptomslist)

    if request.method == 'GET':
        return render(request, 'user/disease_prediction.html', {"list2": alphabaticsymptomslist, 'u':u})

    elif request.method == 'POST':
        symptoms = request.POST.getlist('symtoms')
        print(symptoms)
        noofsym = len(symptoms)
        print(noofsym)
        # access you data by playing around with the request.POST object

        inputno = noofsym
        if (inputno == 0):
            return JsonResponse({'predicteddisease': "none", 'confidencescore': 0})

        else:

            psymptoms = []
            psymptoms = symptoms

            print(psymptoms)

            """      #main code start from here...
            """

            testingsymptoms = []
            # append zero in all coloumn fields...
            for x in range(0, len(symptomslist)):
                testingsymptoms.append(0)

            # update 1 where symptoms gets matched...
            for k in range(0, len(symptomslist)):

                for z in psymptoms:
                    if (z == symptomslist[k]):
                        testingsymptoms[k] = 1

            inputtest = [testingsymptoms]

            print(inputtest)

            model = nn.Sequential(
                nn.Linear(in_features=132, out_features=41),
                nn.Softmax(dim=-1)
            )

            # Load the saved model state_dict
            model.load_state_dict(torch.load('C:\\Users\\admin\\PycharmProjects\\Symptoms_based_disease_prediction\\disease_prediction\\savemodel.pth'))
            model.eval()  # Set the model to evaluation mode

            input_tensor = torch.tensor(inputtest, dtype=torch.float32)

            # Make predictions
            with torch.no_grad():
                output = model(input_tensor)

            # Convert output probabilities to percentages
            prediction_probabilities = output.squeeze().numpy() * 100

            # Define a mapping from output indices to disease names
            # Replace the example diseases with your actual disease names
            disease_mapping = {
                0: '(vertigo) Paroymsal  Positional Vertigo',
                1: 'AIDS',
                2: 'Acne',
                3: 'Alcoholic hepatitis',
                4: 'Allergy',
                5: 'Arthritis',
                6: 'Bronchial Asthma',
                7: 'Cervical spondylosis',
                8: 'Chicken pox',
                9: 'Chronic cholestasis',
                10: 'Common Cold',
                11: 'Dengue',
                12: 'Diabetes ',
                13: 'Dimorphic hemmorhoids(piles)',
                14: 'Drug Reaction',
                15: 'Fungal infection',
                16: 'GERD',
                17: 'Gastroenteritis',
                18: 'Heart attack',
                19: 'Hepatitis B',
                20: 'Hepatitis C',
                21: 'Hepatitis D',
                22: 'Hepatitis E',
                23: 'Hypertension ',
                24: 'Hyperthyroidism',
                25: 'Hypoglycemia',
                26: 'Hypothyroidism',
                27: 'Impetigo',
                28: 'Jaundice',
                29: 'Malaria',
                30: 'Migraine',
                31: 'Osteoarthristis',
                32: 'Paralysis (brain hemorrhage)',
                33: 'Peptic ulcer diseae',
                34: 'Pneumonia',
                35: 'Psoriasis',
                36: 'Tuberculosis',
                37: 'Typhoid',
                38: 'Urinary tract infection',
                39: 'Varicose veins',
                40: 'hepatitis A'
                # Add more mappings as needed
            }

            # Sort the probabilities in descending order
            sorted_indices = np.argsort(prediction_probabilities)[::-1]

            # Print the top 5 diseases with highest probabilities
            predicted_disease = []
            score = []
            for pd in sorted_indices[:5]:
                disease_name = disease_mapping[pd]
                prob = prediction_probabilities[pd]
                rprob = round(prob, 2)
                predicted_disease.append(disease_name)
                score.append(str(rprob))

                print(f'{disease_name}: {prob:.2f}%')

            # consult_doctor codes----------

            #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
            #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]

            Rheumatologist = ['Osteoarthristis', 'Arthritis']

            Cardiologist = ['Heart attack', 'Bronchial Asthma', 'Hypertension ']

            ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo', 'Hypothyroidism']

            Orthopedist = []

            Neurologist = ['Varicose veins', 'Paralysis (brain hemorrhage)', 'Migraine', 'Cervical spondylosis']

            Allergist_Immunologist = ['Allergy', 'Pneumonia',
                                      'AIDS', 'Common Cold', 'Tuberculosis', 'Malaria', 'Dengue', 'Typhoid']

            Urologist = ['Urinary tract infection',
                         'Dimorphic hemmorhoids(piles)']

            Dermatologist = ['Acne', 'Chicken pox', 'Fungal infection', 'Psoriasis', 'Impetigo']

            Gastroenterologist = ['Peptic ulcer diseae', 'GERD', 'Chronic cholestasis', 'Drug Reaction',
                                  'Gastroenteritis', 'Hepatitis E',
                                  'Alcoholic hepatitis', 'Jaundice', 'hepatitis A',
                                  'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Diabetes ', 'Hypoglycemia']

            if predicted_disease[0] in Rheumatologist:
                consultdoctor = "Rheumatologist"

            if predicted_disease[0] in Cardiologist:
                consultdoctor = "Cardiologist"


            elif predicted_disease[0] in ENT_specialist:
                consultdoctor = "ENT specialist"

            elif predicted_disease[0] in Orthopedist:
                consultdoctor = "Orthopedist"

            elif predicted_disease[0] in Neurologist:
                consultdoctor = "Neurologist"

            elif predicted_disease[0] in Allergist_Immunologist:
                consultdoctor = "Allergist/Immunologist"

            elif predicted_disease[0] in Urologist:
                consultdoctor = "Urologist"

            elif predicted_disease[0] in Dermatologist:
                consultdoctor = "Dermatologist"

            elif predicted_disease[0] in Gastroenterologist:
                consultdoctor = "Gastroenterologist"

            else:
                consultdoctor = "other"

            request.session['doctortype'] = consultdoctor

            patientusername = u.user.username
            puser = User.objects.get(username=patientusername)

            # saving to database.....................

            patient = puser.usermodel
            diseasename = predicted_disease
            no_of_symp = inputno
            symptomsname = psymptoms
            confidence = score
            d1 = Decimal(score[0])
            d2 = Decimal(score[1])
            d3 = Decimal(score[2])
            d4 = Decimal(score[3])
            d5 = Decimal(score[4])

            diseasescan_new = Diseasescan(patient=patient, diseasename1=predicted_disease[0],
                                            diseasename2=predicted_disease[1], diseasename3=predicted_disease[2],
                                            diseasename4=predicted_disease[3], diseasename5=predicted_disease[4],
                                            no_of_symp=no_of_symp,
                                            symptomsname=symptomsname,
                                            confidence1=d1,
                                            confidence2=d2,
                                            confidence3=d3,
                                            confidence4=d4,
                                            confidence5=d5,
                                            consultdoctor=consultdoctor)
            diseasescan_new.save()

            request.session['diseasescan_id'] = diseasescan_new.id

            print("disease record saved sucessfully.............................")
            return redirect('disease')
            # return JsonResponse({'diseasename1': predicted_disease[0], 'diseasename2': predicted_disease[1],
            #                      'diseasename3': predicted_disease[2], 'diseasename4': predicted_disease[3],
            #                      'diseasename5': predicted_disease[4],
            #                      'confidence1': d1, 'confidence2': d2, 'confidence3': d3, 'confidence4': d4,
            #                      'confidence5': d5, "consultdoctor": consultdoctor})

    return render(request, 'user/disease_prediction.html', {'u':u})


def disease(request):
    user = request.user.id
    u = Usermodel.objects.get(user=user)

    uid = Diseasescan.objects.filter(patient=u).last()
    return render(request, 'user/disease.html',{'u':u, 'uid':uid})

from django.db.models import Avg
def consult_doctor(request):
    user = request.user.id
    u = Usermodel.objects.get(user=user)

    uid = Diseasescan.objects.filter(patient=u).last()
    doctorspe = uid.consultdoctor

    did = Doctor.objects.filter(specialization=doctorspe)

    for doctor in did:
        avg_rating = rating_review.objects.filter(doctor=doctor).aggregate(Avg('rating'))['rating__avg']
        doctor.avg_rating = avg_rating if avg_rating else 0

    return render(request, 'user/consult_doctor.html', {'u':u, 'did':did})


def make_consultation(request, doctorusername):
    user = request.user.id
    u = Usermodel.objects.get(user=user)

    if request.method == 'POST':
        patientusername = u.user.username
        puser = User.objects.get(username=patientusername)
        patient_obj = puser.usermodel

        # doctorusername = request.session['doctorusername']
        duser = User.objects.get(username=doctorusername)
        doctor_obj = duser.doctor
        request.session['doctorusername'] = doctorusername

        diseasescan_id = request.session['diseasescan_id']
        diseasescan_obj = Diseasescan.objects.get(id=diseasescan_id)

        consultation_date = date.today()
        status = "active"

        consultation_new = consultation(patient=patient_obj, doctor=doctor_obj, diseaseinfo=diseasescan_obj,
                                        consultation_date=consultation_date, status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id

        print("consultation record is saved sucessfully.............................")

        return redirect('consultationview', consultation_new.id)


def consultationview(request, consultation_id):
    user = request.user.id
    u = Usermodel.objects.get(user=user)
    user = request.user
    userp = Usermodel.objects.get(user=user)
    x = userp.user
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
            'x': x,
            'consultation_id':consultation_id
        }
        return render(request, 'user/chat.html', context)


def chat(request):
    user = request.user.id
    u = Usermodel.objects.get(user=user)
    if request.method == "POST":
        msg = request.POST['chat-msg']
        consultation_id = request.session['consultation_id']
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj, sender=request.user, message=msg)

        if msg != '':
            c.save()
            print("msg saved" + msg)
            return redirect('chat_messages')
        else:
            return HttpResponse('Request must be POST.')

    return render(request, 'user/chat.html',{'u':u})

def chat_messages(request):
    user = request.user.id
    u = Usermodel.objects.get(user=user)
    user = request.user
    userp = Usermodel.objects.get(user=user)
    x = userp.user

    if request.method == "GET":
        consultation_id = request.session['consultation_id']
        all_messages = Chat.objects.filter(consultation_id=consultation_id)
        all_messages = sorted(all_messages, key=attrgetter('created') )
        c = Chat.objects.filter(consultation_id=consultation_id, sender=x)
        other_user_msgs = Chat.objects.filter(consultation_id=consultation_id).exclude(sender=x)
        consultation_obj = consultation.objects.get(id=consultation_id)

        context = {
            'msg': c,
            'u': u,
            'other_user_msgs': other_user_msgs,
            'consultation_obj': consultation_obj,
            'all_messages': all_messages,
            'x': x,
            'consultation_id':consultation_id
        }

        return render(request, 'user/chat.html', context)


def doctor_review(request, consultation_id):
    user = request.user.id
    u = Usermodel.objects.get(user=user)
    if request.method == "POST":
        consultation_obj = consultation.objects.get(id=consultation_id)
        patient = consultation_obj.patient
        doctor = consultation_obj.doctor
        rating = request.POST['rate']
        review = request.POST['feedback']

        rating_obj = rating_review(patient=patient, doctor=doctor, rating=rating, review=review)
        rating_obj.save()

        return redirect('consultation_history')

    return render(request, 'user/doctor_review.html',{'u':u})