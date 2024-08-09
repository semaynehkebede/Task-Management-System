from rest_framework import serializers

from tms_api.models import CUser, Project


class GetEmployeeSerializer(serializers.ModelSerializer):
  class Meta:
    model = CUser
    # fields = ['id', 'email', 'firstName', 'secondName', 'lastName', 'gender', 'age', 'is_active', 'role', 'phoneNumber', 'jobTitle', 'title', 'archiveReason']
    fields = '__all__'

class RegisterEmployeeSerializer(serializers.ModelSerializer):
    # We are writing this because we need confirm password field in our Registratin Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = CUser
    fields = ['email', 'firstName', 'secondName', 'lastName', 'gender', 'createdBy', 'archiveReason', 'age', 'role', 'phoneNumber', 'jobTitle', 'title', 'password', 'password2']
    extra_kwargs={
      'password':{'write_only':True}
    }
  # Validating Password and Confirm Password while Registration
  def validate(self, data):
    password = data.get('password')
    password2 = data.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password does not match")
    return data

  def create(self, validate_data):
    return CUser.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = CUser
    fields = ['email', 'password']

class ProjectsSerializer(serializers.ModelSerializer):
  createdBy = GetEmployeeSerializer()
  
  class Meta:
    model = Project
    fields = '__all__'

class CreateProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = ['title', 'description', 'isActive', 'createdBy', 'archiveReason']