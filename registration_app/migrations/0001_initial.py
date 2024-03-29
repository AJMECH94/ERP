# Generated by Django 4.1.7 on 2023-03-26 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(choices=[('Production', 'Production'), ('Maintance', 'Maintance'), ('Accounts', 'Accounts')], max_length=25)),
                ('description', models.TextField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('is_send', models.BooleanField(default=False)),
                ('created_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_up_email', models.EmailField(max_length=250, unique=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('marital_status', models.CharField(choices=[('Married', 'Married'), ('Un-Married', 'Un-Married')], max_length=10)),
                ('join_date', models.DateField(blank=True, null=True)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('skills', models.CharField(choices=[('Python', 'Python'), ('Java', 'Java'), ('Database', 'Database')], max_length=50)),
                ('contact_no', models.PositiveIntegerField(blank=True, null=True)),
                ('uan_number', models.IntegerField(blank=True, null=True)),
                ('uploaded_aadhar', models.FileField(blank=True, null=True, upload_to='aadhar')),
                ('uploaded_cv', models.FileField(blank=True, null=True, upload_to='CV')),
                ('emp_photo', models.ImageField(blank=True, null=True, upload_to='emp_photo')),
                ('address', models.CharField(max_length=100)),
                ('department_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='department_info', to='registration_app.departmentmodel')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('employee_code', models.CharField(max_length=10)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
                ('user_role', models.CharField(choices=[('On Pay Roll', 'On Pay Roll'), ('On Contract Roll', 'On Contract Roll')], max_length=20)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('user_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_details_status', to='registration_app.userdetailsmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
