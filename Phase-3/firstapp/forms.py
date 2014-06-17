from django import forms
from models import Course

class CourseAddForm(forms.ModelForm):
	class Meta:
		model = Course
