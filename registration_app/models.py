from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)    

CONTRACT_TYPE = (
    ('On Pay Roll','On Pay Roll'),
    ('On Contract Roll','On Contract Roll')
    )

USER_ROLES = (
    ("Admin","Admin"),
    ("Employee","Employee")
)

GENDER_CHOICE = (
    ('Male','Male'),
    ('Female','Female')
)

MARTIAL_STATUS = (
    ('Married','Married'),
    ('Un-Married','Un-Married')
)

SKILL_INFO = (
    ('Python','Python'),
    ('Java','Java'),
    ('Database','Database')
)

DEPARTMENT_NAMES = (
    ('Production',"Production"),
    ('Maintance',"Maintance"),
    ('Accounts','Accounts')
)

Education = (
    ('10th','10th'),
    ('12th','12th'),
    ('Diploma','Diploma'),
    ('Degree','Degree')
)

class DepartmentModel(models.Model):
    department_name = models.CharField(max_length=25,choices=DEPARTMENT_NAMES)
    description = models.TextField(max_length=250,blank=True,null=True)
    
    def __str__(self) -> str:
        return self.department_name
    
class NotificationModel(models.Model):
    title = models.CharField(max_length=150,blank=False,null=False)
    is_send = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
class UserDetailsModel(models.Model):
    """
    contains user detailed info
    """
    sign_up_email = models.EmailField(max_length=250,unique=True)
    date_of_birth = models.DateField(null=True,blank=True)
    marital_status = models.CharField(max_length=10,choices=MARTIAL_STATUS,null=False,blank=False)
    join_date = models.DateField(null=True,blank=True)
    experience = models.IntegerField(null=True,blank=True)
    skills = models.CharField(max_length=50,choices=SKILL_INFO)
    contact_no = models.PositiveIntegerField(null=True,blank=True)
    uan_number = models.IntegerField(blank=True,null=True)
    department_details = models.ForeignKey(DepartmentModel,on_delete=models.CASCADE,related_name='department_info')
    uploaded_aadhar = models.FileField(upload_to='aadhar',blank=True,null=True)
    uploaded_cv = models.FileField(upload_to='CV',blank=True,null=True)
    emp_photo = models.ImageField(upload_to='emp_photo',blank=True,null=True)
    address = models.CharField(max_length=100,blank=False,null=False)
    education_details = models.CharField(max_length=10, choices=Education,blank=True,null=True)
    
    def __str__(self):
        return self.sign_up_email
    
class MyUserManager(BaseUserManager):
    """
    Class for customizing the User Model objects manager class
    """

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
 
        )
        user.is_admin = True
        user.user_role = "Admin"
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        # user.password = make_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    employee_code = models.CharField(max_length=10,null=False,blank=False)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICE)
    first_name = models.CharField(max_length=25,blank=False,null=False)
    last_name = models.CharField(max_length=25,blank=False,null=False)
    contract_type = models.CharField(max_length=30,choices=CONTRACT_TYPE)
    user_role = models.CharField(max_length=20,choices=USER_ROLES,default="Employee")
    user_details = models.ForeignKey(UserDetailsModel,on_delete=models.CASCADE,related_name='user_details_status',
                                     blank=True,null=True)
    # notification_details = models.ForeignKey(NotificationModel,on_delete=models.CASCADE,related_name='notification_status',
    #                                          null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    