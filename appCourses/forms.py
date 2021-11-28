from django import forms
from .models import Course

class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'course_name',
            'course_image',
            'faculty_details',
            'course_description',
            'start_date',
            'end_date',
        ]


    # Logic for raising error if end_date < start_date
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")