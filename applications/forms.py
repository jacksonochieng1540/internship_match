from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter', 'portfolio', 'certificates']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 4}),
        }
