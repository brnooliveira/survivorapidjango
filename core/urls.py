from django.urls import path
from .views import add_survivor, profile, SurvivorAPIView, InfectedSurvivorView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('registration/add-survivor/', add_survivor, name='add_survivor'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('profile/', profile, name='profile'),
    path('survivors/', SurvivorAPIView.as_view(), name='survivors'),
    path('survivors/<int:pk>', SurvivorAPIView.as_view()),
    path('infected/', InfectedSurvivorView.as_view(),
         name='infected-survivor-list'),
]
