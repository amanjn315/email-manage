from django.urls import path
from send.views import (
    index,
    login_view,
    logout_view,
    profile_upload,
    send_view
)

urlpatterns = [
    path('',index,name="index"),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('profile_upload/',profile_upload,name='profile_upload'),
    path('send/',send_view,name='send'),

]
