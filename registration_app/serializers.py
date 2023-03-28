from rest_framework import serializers
from registration_app.models import User,UserDetailsModel,DepartmentModel
from django.contrib.auth.hashers import make_password
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailsModel
        fields = '__all__'
        
class GetUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['employee_code','gender','first_name','last_name','contract_type','user_role']
    
    def to_representation(self, instance):
        response_data = super().to_representation(instance)
        print('=============',instance.__dict__)
        user_detail_obj = UserDetailsModel.objects.get(sign_up_email=instance.email)
        response_data['date_of_birth'] = user_detail_obj.date_of_birth
        response_data['marital_status'] = user_detail_obj.marital_status
        response_data['join_date'] = user_detail_obj.join_date
        response_data['experience'] = user_detail_obj.experience
        response_data['skills'] = user_detail_obj.skills
        response_data['contact_no'] = user_detail_obj.contact_no
        response_data['uan_number'] = user_detail_obj.uan_number
        response_data['department_name'] = user_detail_obj.department_details.department_name
        try:
            response_data['uploaded_aadhar'] = user_detail_obj.uploaded_aadhar.path
            response_data['uploaded_cv'] = user_detail_obj.uploaded_cv.path
            response_data['emp_photo'] = user_detail_obj.emp_photo.path
        except:
            pass
        response_data['address'] = user_detail_obj.address
        response_data['education'] = user_detail_obj.education_details
        return response_data
        
class UserDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetailsModel
        fields = ['date_of_birth','marital_status','skills','contact_no','uan_number','uploaded_aadhar',\
            'uploaded_cv','emp_photo','address','education_details']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        # print('validated_data',validated_data)
        hash_password = make_password(password=validated_data['password'])
        validated_data['password'] = hash_password
        print('validated_data',validated_data)
        return super().create(validated_data)
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentModel
        fields = '__all__'

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs
  

# class SendPasswordResetEmailSerializer(serializers.Serializer):
#   email = serializers.EmailField(max_length=255)
#   class Meta:
#     fields = ['email']

#   def validate(self, attrs):
#     email = attrs.get('email')
#     if User.objects.filter(email=email).exists():
#       user = User.objects.get(email = email)
#       uid = urlsafe_base64_encode(force_bytes(user.id))
#       print('Encoded UID', uid)
#       token = PasswordResetTokenGenerator().make_token(user)
#       print('Password Reset Token', token)
#       link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
#       print('Password Reset Link', link)
#       # Send EMail
#       body = 'Click Following Link to Reset Your Password '+link
#       data = {
#         'subject':'Reset Your Password',
#         'body':body,
#         'to_email':user.email
#       }
#       # Util.send_email(data)
#       return attrs
#     else:
#       raise serializers.ValidationError('You are not a Registered User')