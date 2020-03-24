from django.urls import path
from accounts import views
app_name="accounts"


urlpatterns=[
path('',views.Registration,name="register"),
path('activate/<uidb64>/<token>/',views.ActivateView,name="activate")
]
