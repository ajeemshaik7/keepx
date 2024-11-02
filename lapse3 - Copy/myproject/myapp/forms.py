from django import forms
from .models import UserContent

class UserContentForm(forms.ModelForm):
    class  Meta:
        model=UserContent
        fields=['content']
        widgets={
            'content':forms.Textarea(attrs={'class':'form-control','rows':10,'cols':100})
        }
