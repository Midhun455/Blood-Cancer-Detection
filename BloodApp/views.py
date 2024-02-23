from json import load
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login
from requests import session
from .models import *

# Create your views here.


def index(request):
    docData = Doctor.objects.filter(loginid__is_active=0)
    print(docData)
    return render(request, "index.html", {"docData": docData})


def patientReg(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        password = request.POST["password"]
        image = request.FILES["imgfile"]

        if not Login.objects.filter(username=email).exists():
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="Patient",
                viewPass=password,
            )
            logQry.save()

            if logQry:
                regQry = Patient.objects.create(
                    name=name,
                    email=email,
                    gender=gender,
                    phone=phone,
                    dob=dob,
                    image=image,
                    address=address,
                    loginid=logQry,
                )
                regQry.save()
                if regQry:
                    return HttpResponse(
                        "<script>alert('Registration Successful');window.location.href='/login';</script>"
                    )
        else:
            return HttpResponse(
                "<script>alert('Email Already Exists');window.location.href='/doctorReg';</script>"
            )
    return render(request, "COMMON/patientReg.html")


def signin(request):
    if request.POST:
        email = request.POST["email"]
        password = request.POST["password"]
        if Login.objects.filter(username=email, viewPass=password).exists():
            data = authenticate(username=email, password=password)
            if data is not None:
                login(request, data)
                if data.userType == "Patient":
                    id = data.id
                    request.session["uid"] = id
                    resp = '<script>alert("Login Success"); window.location.href = "/userhome";</script>'
                    return HttpResponse(resp)
                elif data.userType == "Doctor":
                    id = data.id
                    request.session["uid"] = id
                    resp = '<script>alert("Login Success"); window.location.href = "/doctorHome";</script>'
                    return HttpResponse(resp)
                elif data.userType == "Hospital":
                    id = data.id
                    request.session["uid"] = id
                    resp = '<script>alert("Login Success"); window.location.href = "/hospitalhome";</script>'
                    return HttpResponse(resp)
                elif data.userType == "Admin":
                    resp = '<script>alert("Login Success"); window.location.href = "/adminHome";</script>'
                    return HttpResponse(resp)
            else:
                return HttpResponse(
                    "<script>alert('You are not Approved');window.location.href='/login'</script>"
                )
        else:
            return HttpResponse(
                "<script>alert('Invalid Username/Password');window.location.href='/login'</script>"
            )
    return render(request, "COMMON/login.html")


################################- ADMIN -##############################################


def adminHome(request):
    return render(request, "ADMIN/adminHome.html")


def addHospital(request):
    data = Hospital.objects.all()
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        image = request.FILES["imgfile"]

        if not Login.objects.filter(username=email).exists():
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="Hospital",
                viewPass=password,
                is_active=1,
            )
            logQry.save()
            if logQry:
                regQry = Hospital.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    image=image,
                    address=address,
                    loginid=logQry,
                )
                regQry.save()
                if regQry:
                    return HttpResponse(
                        "<script>alert('Added Successfully');window.location.href='/addhospital';</script>"
                    )
        else:
            return HttpResponse(
                "<script>alert('Email Already Exists');window.location.href='/addhospital';</script>"
            )
    return render(request, "ADMIN/addHospital.html", {"data": data})


def updateHospital(request):
    id = request.GET["id"]
    data = Hospital.objects.get(loginid=id)
    logData = Login.objects.get(id=id)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        password = request.POST["password"]
        image = request.FILES.get("imgfile")

        data.name = name
        data.email = email
        data.phone = phone
        data.address = address
        if image:
            data.image = image
            data.save()
        data.save()
        if password:
            logData.set_password(password)
        logData.username = email
        logData.save()
        return HttpResponse(
            "<script>alert('Updated Successfully');window.location.href='/addhospital';</script>"
        )

    return render(request, "ADMIN/updateHospital.html", {"data": data})


def deleteHospital(request):
    id = request.GET["id"]
    deleteData = Login.objects.filter(id=id).delete()
    return HttpResponse(
        "<script>alert('Deleted');window.location.href='/addhospital';</script>"
    )


def viewPatients(request):
    docData = Patient.objects.all()
    print(docData)
    return render(request, "ADMIN/viewPatients.html", {"docData": docData})


################################- HOSPITAL -##############################################


def hospitalHome(request):
    return render(request, "HOSPITAL/hospitalHome.html")


def doctorReg(request):
    uid = request.session["uid"]
    UID = Hospital.objects.get(loginid=uid)
    data = Doctor.objects.filter(hopitalid__loginid=uid)
    print(data)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        specialization = request.POST["specialization"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        password = request.POST["password"]
        image = request.FILES["imgfile"]

        if not Login.objects.filter(username=email).exists():
            logQry = Login.objects.create_user(
                username=email,
                password=password,
                userType="Doctor",
                viewPass=password,
                is_active=1,
            )
            logQry.save()
            if logQry:
                regQry = Doctor.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    specialization=specialization,
                    gender=gender,
                    image=image,
                    address=address,
                    loginid=logQry,
                    hospitalid=UID,
                )
                regQry.save()
                if regQry:
                    return HttpResponse(
                        "<script>alert('Registration Successful');window.location.href='/doctorReg';</script>"
                    )
        else:
            return HttpResponse(
                "<script>alert('Email Already Exists');window.location.href='/doctorReg';</script>"
            )
    return render(request, "COMMON/doctorReg.html", {"data": data})


def deleteDoctor(request):
    id = request.GET["id"]
    deleteData = Login.objects.filter(id=id).delete()
    return HttpResponse(
        "<script>alert('Deleted');window.location.href='/doctorReg';</script>"
    )


################################- PATIENTS -##############################################


def userHome(request):
    return render(request, "USER/userHome.html")


def predict(request):
    uid = request.session["uid"]
    user = Patient.objects.get(loginid=uid)
    data = Doctor.objects.all()
    print(user)
    if request.method == "POST":
        imagefile = request.FILES.get("imagefile")
        if imagefile:
            prediction = predict_image(imagefile)
            print(prediction)
            p = Prediction.objects.create(
                image=imagefile, result=prediction[0], user=user
            )
            p.save()
            image_path = p.image
            return render(
                request,
                "USER/predict.html",
                {"prediction": prediction, "image_path": image_path, "data": data},
            )
    if "book" in request.POST:
        date = request.POST["date"]
        did = request.POST["did"]
        DID = Doctor.objects.get(id=did)

        booknow = Appointments.objects.create(user=user, doctor=DID, date=date)
        booknow.save()
        return HttpResponse(
            "<script>alert('Successfully Booked');window.location.href='/myBookings';</script>"
        )

    return render(request, "USER/predict.html")


def myBookings(request):
    uid = request.session["uid"]
    data = Appointments.objects.filter(user=uid)
    return render(request, "USER/myBookings.html", {"data": data})


###############   DOCTOR  ##################


def doctorHome(request):
    return render(request, "DOCTOR/doctorHome.html")


def docBookings(request):
    uid = request.session["uid"]
    data = Appointments.objects.filter(doctor__loginid=uid)
    print(data)
    return render(request, "DOCTOR/myBookings.html", {"data": data})


###############   DETECTION  ##################

# %%
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
import matplotlib.pyplot as plt
from io import BytesIO


def predict_image(imagefile):
    resultFinal = ""
    # %%
    model = load_model("weights.hdf5")
    model.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    # %%
    img = image.load_img(BytesIO(imagefile.read()), target_size=(150, 150))
    imgplot = plt.imshow(img)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    predictions = model.predict(images, batch_size=10)
    classes = np.argmax(predictions, axis=1)

    if classes == [1]:
        resultFinal = "Cancer"
    else:
        resultFinal = "Normal"
    return resultFinal
