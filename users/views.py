import os
import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import (Admin, Applicant, Director, GeneralAffairs,
                          ProjectManager, User)
from users.serializers import (AdminSerializer2, ApplicantSerializer,
                               ApplicantSerializer2, DirectorSerializer2,
                               GeneralAffairsSerializer2,
                               ProjectManagerSerializer2, RegisterSerializer,
                               UserSerializer)

from .permissions import IsAdmin
from .tokens import account_activation_token


# Create your views here.
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserView(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def postUserView(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def getAllActiveUserView(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Set the number of items per page
    name = request.query_params.get('name', None).lower()
    role = request.query_params.get('role', None)
    active = request.query_params.get('active', None)
    if role and name and active:
        users = User.objects.filter(role=role, name__icontains=name, is_active=active).order_by("user_id")
    elif role and active:
        users = User.objects.filter(role=role, is_active=active).order_by("user_id")
    elif name and active:
        users = User.objects.filter(name__icontains=name, is_active=active).order_by("user_id")
    elif role and name:
        users = User.objects.filter(role=role, name__icontains=name).order_by("user_id")
    elif role:
        users = User.objects.filter(role=role).order_by("user_id")
    elif name:
        users = User.objects.filter(name__icontains=name).order_by("user_id")
    elif active:
        users = User.objects.filter(is_active=active).order_by("user_id")
    else:
        users = User.objects.all().order_by("user_id")
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def getApplicantFromUserView(request, user_id):
    user = User.objects.get(pk=user_id)
    if user is not None:
        applicant = Applicant.objects.get(user=user)
        serializer = ApplicantSerializer2(applicant)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response("User is not found", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getUserFromApplicantView(request, applicant_id):
    applicant = Applicant.objects.get(pk=applicant_id)
    if applicant is not None:
        user = applicant.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response("User is not found", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def adminPostUser(request):
    dataUser = request.data
    email = dataUser['email']
    username = dataUser['username']
    name = dataUser['name']

    # Check if email or username already exists
    if User.objects.filter(Q(email=email) | Q(username=username), is_active=True).exists():
        return Response({'error': 'Email or username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate Random Password
    length = 13
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    password = ''.join(random.choice(chars) for i in range(length))
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.email_is_verified = True
        user.set_password(password)
        user.save()
        
        role = user.role
        if role == 'Director':
            director_data = {'user': user.user_id}
            director_serializer = DirectorSerializer2(data=director_data)
            if director_serializer.is_valid():
                director_serializer.save()
            else:
                user.delete()  # Rollback user creation if related model creation fails
                return Response(director_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif role == 'General Affairs':
            general_affairs_data = {'user': user.user_id}
            general_affairs_serializer = GeneralAffairsSerializer2(data=general_affairs_data)
            if general_affairs_serializer.is_valid():
                general_affairs_serializer.save()
            else:
                user.delete()  # Rollback user creation if related model creation fails
                return Response(general_affairs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif role == 'Project Manager':
            project_manager_data = {'user': user.user_id}
            project_manager_serializer = ProjectManagerSerializer2(data=project_manager_data)
            if project_manager_serializer.is_valid():
                project_manager_serializer.save()
            else:
                user.delete()  # Rollback user creation if related model creation fails
                return Response(project_manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif role == 'Admin':
            admin_data = {'user': user.user_id}
            admin_serializer = AdminSerializer2(data=admin_data)
            if admin_serializer.is_valid():
                admin_serializer.save()
            else:
                user.delete()  # Rollback user creation if related model creation fails
                return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Email user initial login information
        views_dir = os.path.dirname(__file__)
        
        html_template_path = os.path.join(views_dir, 'add_user_email.html')
        
        with open(html_template_path, 'r') as file:
            html_message = file.read()
        
        html_message = html_message.replace('{{ name }}', name)
        html_message = html_message.replace('{{ username }}', username)
        html_message = html_message.replace('{{ email }}', email)
        html_message = html_message.replace('{{ password }}', password)
        
        subject = 'Informasi Login Petrakon Indonesia'
        from_email = 'settings.EMAIL_HOST_USER'
        to_email = [email]
        try:
            send_mail(subject, '', from_email, to_email, html_message=html_message)
        except Exception as e:
            return Response({'error': 'Failed to send email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def updateUserRole(request, user_id):
    try:
        user = get_object_or_404(User, pk=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    new_role = request.data.get('role')

    if not new_role:
        return Response({"error": "Role field is required"}, status=status.HTTP_400_BAD_REQUEST)

    if new_role not in dict(User.ROLES).keys():
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    user.role = new_role
    user.save()

    # Check if there is an existing role object for the user's new role
    existing_role = None
    if new_role == 'Director':
        existing_role = Director.objects.filter(user=user).first()
    elif new_role == 'General Affairs':
        existing_role = GeneralAffairs.objects.filter(user=user).first()
    elif new_role == 'Project Manager':
        existing_role = ProjectManager.objects.filter(user=user).first()
    elif new_role == 'Admin':
        existing_role = Admin.objects.filter(user=user).first()
    elif new_role == 'Applicant':
        existing_role = Applicant.objects.filter(user=user).first()

    if existing_role:
        return Response({"message": "User role updated successfully"}, status=status.HTTP_200_OK)

    # Create new role object
    role_data = {'user': user.user_id}
    serializer = None
    if new_role == 'Director':
        serializer = DirectorSerializer2(data=role_data)
    elif new_role == 'General Affairs':
        serializer = GeneralAffairsSerializer2(data=role_data)
    elif new_role == 'Project Manager':
        serializer = ProjectManagerSerializer2(data=role_data)
    elif new_role == 'Admin':
        serializer = AdminSerializer2(data=role_data)
    elif new_role == 'Applicant':
        serializer = ApplicantSerializer2(data=role_data)

    if serializer and serializer.is_valid():
        serializer.save()
        return Response({"message": "User role updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Failed to create new role object"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def deleteUser(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = False
    user.save()
    return Response({"message": "User successfully deactivated"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getProfileDetail(request, id):
    # Retrieve the logged-in user
    user = request.user
    if str(user.id) != id:
        return Response({"error": "You are not authorized to access this resource."}, status=status.HTTP_403_FORBIDDEN)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    if request.method == 'PATCH':
        data = request.data
        user = request.user
        if 'name' in data:
            user.name = data['name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'foto' in data:
            user.foto = data['foto']
            if (user.foto == "null"):
                user.foto == None

        user.save()

        return JsonResponse({'message': 'User profile updated successfully'})

@api_view(['POST'])
def postRegisterView(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = authenticate(username=request.data['username'], password=request.data['password'])
        request.user = user
        verifyEmail(request)

        data = {
            "user": user.user_id
        }
        applicantSerializer = ApplicantSerializer2(data=data)
        if applicantSerializer.is_valid():
            applicantSerializer.save()
            return Response(applicantSerializer.data, status=status.HTTP_200_OK)
        return Response(applicantSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def verifyEmail(request):
    if request.user.email_is_verified != True:
        current_site = get_current_site(request)
        user = request.user
        email = request.user.email
        subject = "Verify Your Email"
        message = render_to_string('email_message.html', {
            'request': request,
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        email = EmailMessage(
            subject, message, to=[email]
        )
        email.content_subtype = 'html'
        email.send()

@api_view(['GET'])
def verifyEmailConfirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_is_verified = True
        user.save()
        return redirect("https://sihire-fe.vercel.app/login/")
    return redirect("https://sihire-fe.vercel.app/login/")

@api_view(['POST'])
def postLoginView(request):
    login_input=request.data.get('login')
    password=request.data.get('password')

    if "@" in login_input:
        user_obj = User.objects.filter(email = login_input, is_active=True).first()
    else:
        user_obj = User.objects.filter(username = login_input, is_active=True).first()
    
    user = authenticate(username = user_obj.username, password = password)

    if user is not None and user.email_is_verified:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'username': user.username, 'user_id': str(user.user_id), 'token': token.key, 'role': user.role}, status=status.HTTP_200_OK, content_type="application/x-javascript")
    elif user.email_is_verified == False:
        return Response({'error': 'Email is not verified. Verify your email first!'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def postLogoutView(request):
        request.user.auth_token.delete()
        logout(request)
        response = JsonResponse({"message": "Logout successful"})
        return response

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def postPasswordChangeView(request):
    username = request.user.username
    user = authenticate(username=username, password=request.data["old_password"])

    if user is not None:
        if request.data["password"] == request.data["password2"]:
            user.set_password(request.data['password'])
            user.save()

            serializer = UserSerializer(user)
            user_email = user.email

            email = EmailMessage(
                "Change Password Successful", "You have successfully changed your password at sihire!", to=[user_email]
            )
            email.send()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Password didn't match!", status=status.HTTP_400_BAD_REQUEST)
    return Response("Wrong password!", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdmin])
def getUserById(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def getTokenByUser(request, token_key):
    try:
        token = Token.objects.get(key=token_key)
        serializer = UserSerializer(token.user)

        if token.user.role == "Applicant":
            applicant = Applicant.objects.get(user=token.user)
            serializer = ApplicantSerializer(applicant)
            
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "User is not logged in"}, status=status.HTTP_409_UNAUTHORIZED)

@api_view(['GET'])
def getAllEmployee(request):
    name = request.query_params.get('name')
    active = request.query_params.get('active', None)
    
    
    if active is not None:
        active = active.lower() == 'true'


    queryset = User.objects.filter(role__in=['General Affairs', 'Director', 'Project Manager', 'Admin'])
    if name:
        queryset = queryset.filter(name__icontains=name)
    if active is not None:
        queryset = queryset.filter(is_active=active)

    queryset = queryset.order_by("user_id")
    
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllDirector(request):
    name = request.query_params.get('name')
    active = request.query_params.get('active', None)
    
    
    if active is not None:
        active = active.lower() == 'true'


    queryset = User.objects.filter(role__in=['Director'])
    if name:
        queryset = queryset.filter(name__icontains=name)
    if active is not None:
        queryset = queryset.filter(is_active=active)

    queryset = queryset.order_by("user_id")
    
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllProjectManager(request):
    name = request.query_params.get('name')
    active = request.query_params.get('active', None)
    
    
    if active is not None:
        active = active.lower() == 'true'


    queryset = User.objects.filter(role__in=['Project Manager'])
    if name:
        queryset = queryset.filter(name__icontains=name)
    if active is not None:
        queryset = queryset.filter(is_active=active)

    queryset = queryset.order_by("user_id")
    
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)
