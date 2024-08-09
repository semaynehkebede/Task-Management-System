from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from tms_api import views
# from tms_api.views import CreateAccountView, UserLoginView, ViewUserAccountView

urlpatterns = [
    path('', views.index),
    path('users/get-users', views.GetUserView.as_view(), name='getUser'),
    path('users/get-user', views.GetUserByIdView.as_view(), name='getUserById'),
    path('users/create-user', views.RegisterEmployeeView.as_view(), name='registerEmployee'),
    # path('login/', UserLoginView.as_view(), name='login'),
    path('auth/login', views.UserLoginView.as_view(), name='userLogin'),
    path('auth/refresh', TokenRefreshView.as_view(), name='refreshToken'),
    path('projects/get-projects', views.GetProgectsView.as_view(), name='getProjects'),
    path('projects/create-project', views.CreateProgectView.as_view(), name='createProject'),
    path('projects/get-project/<int:id>', views.GetProgectByIdView.as_view(), name='getProjectById'),
    path('projects/update-project/<int:id>', views.UpdateProjectView.as_view(), name='updateProject'),
]