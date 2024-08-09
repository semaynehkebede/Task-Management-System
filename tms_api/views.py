from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.authentication import authenticate
# from django.http import HttpResponse
# from django.contrib.auth import authenticate

from tms_api.authentication import CustomJWTAuthentication
from tms_api.models import CUser, Project
from tms_api.serializer import CreateProjectSerializer, GetEmployeeSerializer, ProjectsSerializer, RegisterEmployeeSerializer, UserLoginSerializer

@api_view(['GET'])
def index(request):
    return Response({"success":"Success Api create"})

class GetUserView(APIView):
  # authentication_classes = [CustomJWTAuthentication]
#   permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    employee=CUser.objects.all()
    serializer = GetEmployeeSerializer(employee, many=True)
    if(serializer.data):
      return Response({'data' : serializer.data, 'count' : len(serializer.data)}, status=201)
    return Response({'status':200, 'payload':"Empty Data"})

class GetUserByIdView(APIView):
  def get(self, request, format = None):
    # employeeId sent by form data from end point as request
    employeeId = request.data.get('employeeId')
    try:
      employee = CUser.objects.get(id=employeeId)
      serializer=GetEmployeeSerializer(employee)
      # authorization_header = request.META.get('HTTP_AUTHORIZATION')
      return Response(serializer.data)
    except CUser.DoesNotExist:
      return Response({"Error": "Employee does not exist"}, status=404)
    except Exception as e:
      return Response({"success": False, "error": str(e)}, status=500)
    

class RegisterEmployeeView(APIView):
  def post(self, request, format=None):
    serializer=RegisterEmployeeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    # token = get_tokens(user)
    # return Response({'token':token, 'message':'Registration Successful'}, status=status.HTTP_201_CREATED)
    return Response({'user':user, 'message':'Registration Successful'}, status=status.HTTP_201_CREATED)
  
  
  
def get_tokens(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }
def get_refresh_tokens(access_token):
  pass

class UserLoginView(APIView):
  def post(self, request):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens(user)
      return Response({'message':'Login Success', 'token':token}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)


class GetProgectsView(APIView):
  def get(self, request, format=None):
    project = Project.objects.all()  
    serializer = ProjectsSerializer(project, many=True)
    if(serializer.data):
      return Response({'data':serializer.data, 'count':len(serializer.data)}, status=200)
    return Response({'detail':'Empty Data'})
  
class CreateProgectView(APIView):
  def post(self, request, format = None):
    serializer = CreateProjectSerializer(data = request.data)
    serializer.is_valid(raise_exception=True)
    project = serializer.save()
    if(project):
      return Response({'success': 'Project Created Successfully', 'project': serializer.data}, status=200)
    return Response({'error':'project not created'}, status=status.HTTP_404_NOT_FOUND)
  
class GetProgectByIdView(APIView):
  def get(self, request, id, format=None):
    # request.user :-  to retrive login user user name
    # request.user.id  :- to retrive login user user id
    if not id:
      return Response({"error": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    project = Project.objects.filter(id=id)
    if not project:
      return Response({"error": "project not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProjectsSerializer(project, many=True)  
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)  
    
class UpdateProjectView(APIView):
  def put(self, request, format = None):
    pass