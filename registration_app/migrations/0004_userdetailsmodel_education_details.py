# Generated by Django 3.2.18 on 2023-03-27 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_app', '0003_alter_user_contract_type_alter_user_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetailsmodel',
            name='Education_details',
            field=models.CharField(blank=True, choices=[('10th', '10th'), ('12th', '12th'), ('Diploma', 'Diploma'), ('Degree', 'Degree')], max_length=10, null=True),
        ),
    ]
