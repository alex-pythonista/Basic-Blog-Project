from django.urls import path
from . import views


app_name = 'login_app'

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),   
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_profile/', views.user_change, name='change_profile'),
    path('password/', views.pass_change, name='change_password'),
    path('add_profile_picture/', views.add_profile_picture, name='add_picture'),
    path('change_profile_picture/', views.change_profile_picture, name='change_picture'),
    path('edit_bio/', views.edit_bio, name='edit_bio'),
]


