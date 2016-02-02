#encoding: utf-8
from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from Users.models import blogUsers
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

    class Meta:
        model = blogUsers
        fields = ['first_name', 'last_name', 'username', 'email']
        
class changeUser(ModelForm):
	class Meta:
		model = User
		fields = ['username','first_name', 'last_name', 'email']
        
	def __init__(self, *args, **kwargs):
	    super(changeUser, self).__init__(*args,**kwargs)	    
	    self.fields['username'].widget.attrs['readonly'] = True
	    self.fields['username'].help_text = None  
	    self.fields['email'].help_text = None  
	    self.fields['first_name'].help_text = None  
	    self.fields['last_name'].help_text = None  	    	    

	    	    	         
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",'first_name', 'last_name')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class editUserA(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email",'first_name', 'last_name','is_staff','is_superuser']

    def __init__(self, *args, **kwargs):
	    super(editUserA, self).__init__(*args,**kwargs)	    
	    self.fields['username'].help_text = None
	    self.fields['email'].help_text = None
	    self.fields['first_name'].help_text = None
	    self.fields['last_name'].help_text = None
	    self.fields['is_staff'].help_text = None
	    self.fields['is_superuser'].help_text = None
	   

