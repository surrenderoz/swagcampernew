import os
import random
import string

import datetime
from django.contrib import auth as adminatuh
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import  messages
from django.contrib.auth.models import User

from .forms import EventForm, AddMediaForm

import firebase_admin
from firebase_admin import credentials, auth, firestore, messaging, storage, db as realtime

cred = credentials.Certificate("swag-f7a2c-firebase-adminsdk-mvzv7-518757bddf.json")
firebase_admin.initialize_app(cred,{
    'storageBucket': 'swag-f7a2c.appspot.com',
    'databaseURL': 'https://swag-f7a2c-default-rtdb.firebaseio.com'
})
db = firestore.client()
bucket = storage.bucket()
ref = realtime.reference('status')



def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = adminatuh.authenticate(username=username,password=password)
        if user is not None:
            adminatuh.login(request,user)
            return redirect('/')
        else:
            return redirect('login')
    return render(request,'login.html')

def logoutView(request):
    adminatuh.logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    users = auth.list_users().iterate_all()
    events = db.collection('events').get()
    finalUser = []
    for user in users:
        finalUser.append(user.uid)
    context = {
        "users": len(finalUser),
        "events": len(events)
    }   
    return render(request, 'home.html', context)

@login_required(login_url='login')
def addEvent(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            imagePath = request.FILES['file']
            blob = bucket.blob(str(imagePath))
            blob.upload_from_file(imagePath, content_type='image/jpg')
            blob.make_public()
            # print(imagePath)
            db.collection('events').document().set({
                "eventName": form.cleaned_data.get('eventname'),
                "eventLocation": form.cleaned_data.get('eventlocation'),
                "eventDate": form.cleaned_data.get('birthday'),
                "eventMessage": form.cleaned_data.get('eventmessage'),
                "img": blob.public_url,
                "createdAt": datetime.datetime.now()
            })
            messages.success(request, 'Added To Database')

        else:
            messages.success(request, 'Added')

    context = {
        "form": form,
        "userslist": auth.list_users().iterate_all()
    }
    return render(request, 'addevent.html', context)


@login_required(login_url='login')
def eventList(request):
    dataN = db.collection('events')
    qs = dataN.order_by(
        u'createdAt', direction=firestore.Query.DESCENDING)
    events = qs.stream()
    # for v in events:
    #     print('cool', v)
    context = {
        "data": events
    }
    return render(request, 'eventlist.html', context)


@login_required(login_url='login')
def bookingList(request):
    dataN = db.collection('bookings')
    qs = dataN.order_by(
        u'createdAt', direction=firestore.Query.DESCENDING)
    bookings = qs.stream()
    context = {
        "data": bookings
    }
    return render(request, 'bookings.html', context)


@login_required(login_url='login')
def deleteEvent(request, pk):
    db.collection('events').document(pk).delete()
    return redirect('eventlist')


@login_required(login_url='login')
def usersList(request):
    if request.method == 'POST':
        getStatus = request.POST.get('status')
        getuserId = request.POST.get('userid')
        setStatus = ref.child(getuserId)
        setStatus.set({
            "key": getuserId,
            "value": getStatus
        })
###########################################################################################################################
    obj = ref.get()
    context = {
        "data": db.collection('users').get(),
        "activestatus": obj
    }
    return render(request, 'users.html', context)


@login_required(login_url='login')
def deleteuser(request, uid):
    # auth.delete_user(uid)
    finuser = auth.list_users().iterate_all()
    for user in finuser:
        if user.email == uid:
            auth.delete_user(user.uid)
    db.collection('users').document(uid).delete()
    return redirect('users')


@login_required(login_url='login')
def deleteBooking(request, uid):
    db.collection('bookings').document(uid).delete()
    return redirect('bookinglist')


# media upod view
@login_required(login_url='login')
def mediaUploadView(request):
    form = AddMediaForm()
    if request.method == 'POST':
        form = AddMediaForm(request.POST, request.FILES)
        if form.is_valid():
            extesionss, ext = os.path.splitext(str(request.FILES['file']))
            imagePath = request.FILES['file']
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(0,5))
            blob = bucket.blob(result_str + str(imagePath))
            blob.upload_from_file(imagePath, content_type=ext)
            blob.make_public()
            # print('hiiiiiiiiii',blob.public_url)
            # print(form.cleaned_data.get('mediaUrl'))

            db.collection('media').document().set({
                "img": blob.public_url,
                "type": ext
            })
           
            print(form.errors)
        # else:
        #     print('erros')
    context = {
        "form": form
    }
    return render(request, 'media.html', context)

# media upod view
@login_required(login_url='login')
def mediaUploadYoutubeView(request):
    if request.method == 'POST':
            db.collection('media').document().set({
                "img": request.POST.get('mediaUrl'),
                "type": 'ytVideo'
            })
    return render(request, 'yt.html')


@login_required(login_url="login")
def mediaView(request):
    data = db.collection('media').get()
    if request.method == 'POST':
        getID = request.POST.get('docid')
        getobj = request.POST.get('obj')
        try:
            db.collection('media').document(getID).delete()
            x = getobj.rsplit('/', 1)
            bucket.blob(x[1]).delete()
            return redirect('gallery')
        except:
            pass

    context = {
        "data": data
    }
    return render(request, 'mediaview.html', context)


@login_required(login_url='login')
def mediaDeleteView(request, id):
    if request.method == 'POST':
        getobj = request.POST.get('obj')
        x = getobj.split('/')
        print(x)
        # bucket.file().delete(id)
    return HttpResponse('done')


@login_required(login_url='login')
def SendMsg(request):
    usersList = db.collection('users').get()
    registration_token = ''
    if request.method == 'POST':
        uids = request.POST.get('userid')
        device = request.POST.get('device')
        title = request.POST.get('title')
        msg = request.POST.get('message')
        frm = request.POST.get('from')
        for user in usersList:
            if user.to_dict()['uid'] == uids:
                registration_token += user.to_dict()['key']
                print(user.to_dict()['key'])
                if user.to_dict()['device'] == "android":
                    message = messaging.Message(
                    android=messaging.AndroidConfig(
                        ttl=datetime.timedelta(seconds=3600),
                        priority='normal',
                        notification=messaging.AndroidNotification(
                            title= title,
                            body= msg
                        ),
                    ),       
                    token=registration_token,
                    )
                else:
                    message = messaging.Message(
                    apns=messaging.APNSConfig(
                        headers={'apns-priority': '10'},
                        payload=messaging.APNSPayload(
                            aps=messaging.Aps(
                                alert=messaging.ApsAlert(
                                    title=title,
                                    body=msg
                                ),
                                badge=42,
                            ),
                        ),
                    ),
                    token=registration_token,
                    )
                
                response = messaging.send(message)
                print(response)
                 # [START apns_message]
                
                # [END apns_message]
                # return message

                db.collection('notification').document().set({
                    "userid": uids,
                    "from": frm,
                    "title": title,
                    "message": msg,
                    "createdAt": datetime.datetime.now()
                })
    # Response is a message ID string.
    context = {
        "userslist": usersList
    }
    return render(request, 'notify.html', context)


login_required(login_url='login')
def notifyListView(request, *args, **kwargs):
    dataN = db.collection('notification')
    qs = dataN.order_by(
        u'createdAt', direction=firestore.Query.DESCENDING)
    noti = qs.stream()
    context = {
        "data": noti,
        "fewUsers": db.collection('users').get()
    }
    return render(request, 'notifyview.html', context)


login_required(login_url='login')
def notifydeletetView(request, uid):
    db.collection('notification').document(uid).delete()
    return redirect('noifyview')


login_required(login_url='login')
def editUser(request, uid):
    data = db.collection('users').get()
    final = []
    docId = ''
    for user in data:
        if user.to_dict()['uid'] == uid:
            final.append(user)
            docId = user.id
    if request.method == 'POST':
        user = request.POST.get('username')
        userphone = request.POST.get('userphone')
        db.collection('users').document(str(docId)).update({
            "name": user,
            "phone": userphone
        })
        return redirect('users')
    context = {
        "data": final
    }
    return render(request, 'editUser.html', context)