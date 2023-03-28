from registration_app.models import User
from django.core.mail import EmailMessage
import os

def generate_employee_code(input_dict):
    user_obj = User.objects.all().order_by('-id').first()
    if not user_obj.employee_code:
        return str(input_dict['department_details'])[:3] + "0001"
    emp_code = str(input_dict['department_details'])[:3] +  str(int(user_obj.employee_code[3:])+1).zfill(4)
    return emp_code


def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('email'),
      to=[data['to_email']]
    )
    email.send()