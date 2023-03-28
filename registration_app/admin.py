from django.contrib import admin
from registration_app.models import User,UserDetailsModel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ('id','email','employee_code', 'first_name','last_name','user_role','is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('employee_code','first_name','last_name','user_role','contract_type')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'employee_code','first_name','last_name','user_role','contract_type'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()
admin.site.register(User, UserAdmin)


class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('id','sign_up_email','date_of_birth', 'marital_status','join_date','experience','skills','contact_no','uan_number','uploaded_aadhar','uploaded_cv','emp_photo','address','education_details')
admin.site.register(UserDetailsModel, UserDetailAdmin)
