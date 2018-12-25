from django import forms
from .views import Employee


class EmployeeForm(forms.ModelForm):

	class Meta:
		model = Employee
		fields = ['first_name', 'middle_name', 'last_name', 
		'position', 'empl_date', 'salary', 'image', 'superviser']

