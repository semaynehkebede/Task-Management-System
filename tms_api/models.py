from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


class Role(models.TextChoices):
    ADMIN = 'admin'
    PROGECTManager='Progect Manager'
    USER = 'user'

#  Custom User Manager
class CUserManager(BaseUserManager):
  def create_user(self, email, firstName, secondName, lastName, jobTitle, role, createdBy, age, phoneNumber, gender, title, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, position, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      employee = self.model(
          email=self.normalize_email(email),
          firstName=firstName,
          secondName=secondName,
          lastName=lastName,
          jobTitle=jobTitle,
        #   archiveReason=archiveReason,
          role=role,
          createdBy=createdBy,
          age=age,
          phoneNumber=phoneNumber,
          gender=gender,
          title=title,
      )

      employee.set_password(password)
      employee.save(using=self._db)
      return employee

  def create_superuser(self, email, firstName, secondName, lastName, jobTitle, role, createdBy, age, phoneNumber, gender, title, password=None):
      """
      Creates and saves a superuser with the given email, name, position, tc and password.
      """
      employee = self.create_user(
          email,
          password=password,
        #   email=self.normalize_email(email),
          firstName=firstName,
          secondName=secondName,
          lastName=lastName,
          jobTitle=jobTitle,
        #   archiveReason=archiveReason,
          role=role,
          createdBy=createdBy,
          age=age,
          phoneNumber=phoneNumber,
          gender=gender,
          title=title,
      )
      employee.is_admin = True
      employee.save(using=self._db)
      return employee
  
#  Custom User Model
class CUser(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  title = models.CharField(max_length=200)
  firstName = models.CharField(max_length=255)
  secondName = models.CharField(max_length=255)
  lastName = models.CharField(max_length=255)
  phoneNumber = models.CharField(max_length=14)
  gender = models.CharField(max_length=20)
  age = models.IntegerField()
  role = models.CharField(max_length=255, choices=Role.choices, default=Role.USER)
  archiveReason = models.TextField(blank=True)
  createdBy = models.CharField(max_length=255)
  updatedBy = models.CharField(max_length=255, null=True)
  deletedBy = models.CharField(max_length=255, null=True)
  jobTitle = models.CharField(max_length=255)
  
#   position = models.CharField(max_length=200)
#   tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = CUserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['firstName', 'secondName', 'lastName', 'phoneNumber', 'gender', 'age', 'role', 'createdBy', 'title', 'jobTitle']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin


class Project(models.Model):
  title=models.CharField(max_length=255)
  description=models.TextField(max_length=1000)
  isActive=models.BooleanField(default=True)
  createdBy=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='projectCreatedBy')
  updatedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projectUpdatedBy', null=True)
  archiveReason=models.CharField(max_length=255, null=True)
  # auto_now_add=True(meanse the value not changed when we update the data)
  createdAt=models.DateTimeField(auto_now_add=True)
  updatedAt=models.DateTimeField(auto_now=True)
  # auto_now=True(meanse the value updated when we update the data)
  deletedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='projectDeletedBy')
  deletedAt=models.DateTimeField(auto_now=True)

  def __str__(self):
      return self.title
  

class taskStatus(models.TextChoices):
    OPEN = 'Open'
    PENDING='Pending'
    COMPLETED = 'Completed'
    ONHOLD = 'On Hold'
class priorityOption(models.TextChoices):
    HIGTH = 'High'
    MEDIUM='Medium'
    LOW = 'Low'
class Task(models.Model):
      # "tags": [
      #   "string"
      # ],
    title=models.CharField(max_length=255)
    description=models.TextField()
    priority = models.CharField(max_length=255, choices=priorityOption.choices)
    dueDate = models.DateField(auto_now_add=True, null=True)
    projectId = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name='onProject')
    status=models.CharField(max_length=80, choices=taskStatus.choices, default=taskStatus.OPEN)
    assignedId=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='assignedTo')
    createdBy=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='taskCreatedBy')
    updatedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taskUpdatedBy', null=True)
    archiveReason=models.CharField(max_length=255, null=True)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    # auto_now=True(meanse the value updated when we update the data)
    deletedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='taskDeletedBy', null=True)
    deletedAt=models.DateTimeField(auto_now=True)