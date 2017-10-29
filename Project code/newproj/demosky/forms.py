
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from demosky.models import UserProfile
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

   
    
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )




    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (

            'first_name',
            'last_name',
            'password'

        )

class UserProfileForm(forms.ModelForm):
    study=forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'What did you study? eg. Software Engineering'
        }))
    work=forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'What work do you do? eg. Software Developer at XYZ company'
        }))

    birthplace=forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Where are you from? eg. Chicago,IL'
        }))
    location=forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Where do you stay? eg. Bloomington,IN'
        }))
    quote= forms.CharField(widget= forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Your favourite quote goes here!'
        }
    ))
    bio= forms.CharField(widget= forms.Textarea(
        attrs={
            'class':'form-control',
            'placeholder': 'Let us know about you! Write something about yourself'
        }
    ))

    class Meta:
        model = UserProfile
        fields = (
                    'study',
                    'work',
                    'location',
                    'birthplace',
                    'quote',
                    'bio',
                    'photo',
                    'token',

                  )

#class ProfilePicForm(forms.ModelForm):
 #   class Meta:
  #      model = UserProfile
   #     fields = (
    #            'Image',

    #   )

