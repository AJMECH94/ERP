from django.shortcuts import render
from rest_framework.response import Response
from registration_app.serializers import UserRegistrationSerializer,UserDetailSerializer,\
    DepartmentSerializer,UserDetailUpdateSerializer,GetUserProfileSerializer,UserChangePasswordSerializer
from registration_app.models import User,UserDetailsModel,DepartmentModel
from django.contrib.auth import authenticate,login
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import status
from Utils.utility import generate_employee_code, send_email
from django.core.mail import EmailMessage
from decouple import config
from django.urls import reverse
from passlib.hash import pbkdf2_sha256
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes

def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# Create your views here.
class AddDepartmentView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    def post(self,request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"Department added !"})
        return Response({"msg":"Something went wrong while add department!"})
            

class UserRegistrationAPI(ModelViewSet):
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = GetUserProfileSerializer
    allwoed_methods = ['post','put']
    
    def create(self,request,*args, **kwargs):
        # if request.user.is_admin:
        input_dict = request.data
        user_detail_dict = dict()
        user_detail_dict['sign_up_email'] = input_dict['email']
        user_detail_dict['date_of_birth'] = input_dict['date_of_birth']
        user_detail_dict['marital_status'] = input_dict['marital_status']
        user_detail_dict['join_date'] = input_dict['join_date']
        user_detail_dict['experience'] = input_dict['experience']
        user_detail_dict['skills'] = input_dict['skills']
        user_detail_dict['contact_no'] = input_dict['contact_no']
        dept_obj = DepartmentModel.objects.get(department_name=input_dict['department_details'])
        user_detail_dict['department_details'] = dept_obj.id
        user_detail_dict['education_details'] = input_dict['education_details']
        try:
            user_detail_dict['uan_number'] = input_dict['uan_number']
            user_detail_dict['uploaded_aadhar'] = input_dict['uploaded_aadhar']
            user_detail_dict['uploaded_cv'] = input_dict['uploaded_cv']
            user_detail_dict['emp_photo'] = input_dict['emp_photo']
        except:
            pass
        user_detail_dict['address'] = input_dict['address']
        
        detail_serializer = UserDetailSerializer(data=user_detail_dict)
        if detail_serializer.is_valid(raise_exception=True):
            detail_serializer.save()
        
        user_dict = dict()
        user_dict['email'] = input_dict['email']
        employee_code = generate_employee_code(input_dict)
        user_dict['employee_code'] = employee_code
        user_dict['gender'] = input_dict['gender']
        user_dict['first_name'] = input_dict['first_name']
        user_dict['last_name'] = input_dict['last_name']
        user_dict['user_role'] = input_dict['user_role']
        user_dict['contract_type'] = input_dict['contract_type']
        user_dict['password'] = input_dict['password']
        user_detail_obj = UserDetailsModel.objects.get(sign_up_email=user_detail_dict['sign_up_email'])
        if user_detail_obj:
            user_dict['user_details'] = user_detail_obj.id

        serializer = UserRegistrationSerializer(data=user_dict)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            # link = settings.EMP_LOGIN_LINK
            # # Send EMail
            # body = f"Your Registration successfully done \n your credntials are \n Username = {user.email} \n Password = {user_dict['password']} \n you can login using {link} \n Thank you"
            # data = {
            #     'subject':'Registration sucessful',
            #     'body':body,
            #     'to_email':user.email
            #         }
            # send_email(data)
            return Response({'token':token,'msg':"User Register Successfully !"},status=status.HTTP_201_CREATED)
        return Response({"msg":'Something went wrong while user registration!'})
        # return Response({"msg":"you do not have permission to performthis action!"})
    
    def update(self,request,*args, **kwargs):
        print(request.data)
        if request.user.user_role == "Employee":
            input_dict = request.data
            user = User.objects.get(id=request.user.id)
            user_detail_id = user.user_details.id
            user_detail_obj = UserDetailsModel.objects.get(pk=user_detail_id)
            if user_detail_obj:
                detail_serializer = UserDetailUpdateSerializer(user_detail_obj,data=input_dict,partial=True)
                if detail_serializer.is_valid(raise_exception=True):
                    detail_serializer.save()
                    return Response({"msg":"profile updated successfully !"})
                return Response({"msg":"you do not have permission!"})
        elif request.user.user_role == "Admin":
            input_dict = request.data
            user = User.objects.get(id=kwargs['pk'])
            user_detail_id = user.user_details.id
            user_detail_obj = UserDetailsModel.objects.get(pk=user_detail_id)
            if user_detail_obj:
                detail_serializer = UserDetailSerializer(user_detail_obj,data=input_dict,partial=True)
                if detail_serializer.is_valid(raise_exception=True):
                    detail_serializer.save()
                    return Response({"msg":"profile updated successfully !"})
                Response({"msg":"Something went wrong while updating employee!"})
        return Response({"msg":"please check user role !"})
    
    def retrive(self, request, *args, **kwargs):
        user_obj = User.objects.get(pk=kwargs['pk'])
        serializer = self.serializer_class(user_obj,context={"request": request})
        output_dict = serializer.data
        return Response({"result":output_dict})
    
    def list(self, request, *args, **kwargs):
        queryset = User.objects.filter(is_deleted=False,is_admin=False)
        serializer = GetUserProfileSerializer(queryset,many=True)
        return Response({"result":serializer.data})
            
            
class UserLoiginAPI(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        user = authenticate(email=email,password=password)
        if not user:
            return Response({"msg":"please provide valid Credentitals!"})
        else:
            login(request,user)
            token = get_tokens_for_user(user)
            return Response({'token':token,"msg":"logged-in Successfully !"},status=status.HTTP_200_OK)
            

class UserChangePasswordView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    if serializer.is_valid(raise_exception=True):
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

# class SendPasswordResetEmailView(APIView):
#   def post(self, request, format=None):
#     serializer = SendPasswordResetEmailSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)