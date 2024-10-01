from django.contrib import admin
from django.urls import path

from users.views import *

urlpatterns = [
    path('post/', postUserView),
    path('get/', getUserView),
    path('register/', postRegisterView),
    path('add-user/', adminPostUser),
    path('edit-user-role/<uuid:user_id>/', updateUserRole),
    path('delete-user/<uuid:user_id>/', deleteUser),
    path('get-all-users/', getAllActiveUserView),
    path('get-profile/<id>/', getProfileDetail),
    path('logged-in/', getUserView),
    path('register/', postRegisterView),
    path('login/', postLoginView),
    path('logout/', postLogoutView),
    path('change-password/', postPasswordChangeView),
    path('verify-email-confirm/<uidb64>/<token>/', verifyEmailConfirm, name='verify-email-confirm'),
    path('get-applicant/<user_id>/', getApplicantFromUserView),
    path('get-user/<applicant_id>/', getUserFromApplicantView),
    path('get-user-by-id/<user_id>/', getUserById),
    path('get-user-by-token/<str:token_key>/', getTokenByUser),
    path('edit-my-profile/', updateUserProfile),
    path('get-all-employee/', getAllEmployee),
    path('get-all-director/', getAllDirector),
    path('get-all-pm/', getAllProjectManager)
]
