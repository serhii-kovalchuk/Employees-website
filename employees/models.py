from django.db import models
from django.utils import timezone


class Employee(models.Model):

	first_name = models.CharField(max_length=30)
	middle_name = models.CharField(max_length=7)
	last_name = models.CharField(max_length=30)
	position = models.CharField(max_length=7)
	empl_date = models.DateField(default=timezone.now)
	salary = models.PositiveIntegerField()
	image = models.ImageField(default='default.png', 
		upload_to='profile_pics')
	superviser = models.ForeignKey('self', null=True, 
		on_delete=models.CASCADE)
