
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from demosky.models import UserProfile
from django import forms
#code written by shantanu#

class UploadFileForm(forms.Form):       #form to upload files in database
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class RegistrationForm(UserCreationForm):   #user registeration form.
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




    def save(self, commit=True): # form to save data of user in userprofile when generating database
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm): #form to edit profile form
    class Meta:
        model = User
        fields = (

            'first_name',
            'last_name',
            'password'

        )

class UserProfileForm(forms.ModelForm):     #Edit profile form
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

    class Meta:         #class to store the order in userprofile
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



# code written by shantanu ends#