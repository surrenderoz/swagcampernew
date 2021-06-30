from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('login', views.loginView, name="login"),
    path('logout', views.logoutView, name="logout"),
    path('users', views.usersList, name="users"),
    path('deleteuser/<str:uid>', views.deleteuser, name="deleteuser"),
    path('addevent', views.addEvent, name="addevent"),
    path('eventlist', views.eventList, name="eventlist"),
    path('bookinglist', views.bookingList, name="bookinglist"),
    path('deleteEvent/<str:pk>', views.deleteEvent, name="deleteEvent"),
    path('mediaupload', views.mediaUploadView, name="mediaupload"),
    path('yt', views.mediaUploadYoutubeView, name="yt"),
    path('gallery', views.mediaView, name="gallery"),
    path('mediadelete/<str:id>', views.mediaDeleteView, name="mediadelete"),
    path('sendmsg', views.SendMsg, name="sendmsg"),
    path('noifyview', views.notifyListView, name="noifyview"),
    path('deletenoti/<str:uid>', views.notifydeletetView, name="deletenoti"),
    path('editUser/<str:uid>', views.editUser, name="editUser"),
    path('deleteBooking/<str:uid>', views.deleteBooking, name="deleteBooking")
]
