from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from . import models


class CustomBoundField(forms.BoundField):
    
    def label_tag(self, contents=None, attrs=None, label_suffix="", tag=None):
        attrs = attrs or {}
        attrs["class"] = "form-label fw-bold mb-0 text-dark"
        return super().label_tag(contents, attrs, label_suffix, tag)

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        label="First Name:",
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'John',
        })
    )

    last_name = forms.CharField(
        max_length=100,
        label="Last Name:",
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Doe',
        })
    )
    
    middle_name = forms.CharField(
        max_length=100,
        label="Middle Name:",
        required=True,
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Santos',
        })
    )

    email = forms.EmailField(
        max_length=255,
        label="Email:",
        required=True,
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'johdoe@email.com',
        })
    )

    password1 = forms.CharField(
        required=True,
        label="Password:",
        widget=forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder': '•••••••••',
        })
    )
    
    password2 = forms.CharField(
        required=True,
        label="Confirm Password:",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '•••••••••',
        })
    )
    
    class Meta:
        model = models.CustomUser
        fields = ['first_name', 'last_name', 'middle_name','email', 'password1', 'password2',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop('autofocus', None)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if models.CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in used.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name and last_name:
            if models.CustomUser.objects.filter(first_name=first_name, last_name=last_name).exists():
                self.add_error("first_name", "A user with this full name is already registered.")
        return cleaned_data
    
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email:",
        required=True,
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'johndoe@email.com',
        })
    )

    password = forms.CharField(
        required=True,
        label="Password:",
        widget=forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder': '•••••••••',
        })
    )
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class ScholarForm(forms.ModelForm):
    
    bound_field_class = CustomBoundField

    scholarship_name = forms.CharField(
        required=True,
        label="Scholarship Name",
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'Iskolar ng Bayan Program'
        })
    )
    
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'placeholder': 'Enter a brief description of the scholarship...',
            'rows':4
        })
    )
    
    eligibility = forms.MultipleChoiceField(
        choices=models.Residence.choices,
        required=True,
        label="Who Can Apply",
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control  ',
        })
    )
    
    deadline = forms.DateField(
        label="Deadline of scholarship",
        required=True,
        widget=forms.DateInput(attrs={
            'class':'form-control',
            'type':'date'
        })
    )
    
    grant_officer = forms.CharField(
        required=True,
        label="Grants Officer/Scholarship Committee",
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'Camarines Norte PGCEAP'
        })
    )
    
    requirements = forms.CharField(
        label="Scholarship Requirements",
        widget=forms.Textarea(attrs={
            'class':'form-control',
            'placeholder': 'Enter requirement for this scholarship',
            'rows':4
        })
    )
    
    status = forms.ChoiceField(
        choices=models.Status.choices,
        initial=models.Status.OPEN,
        label="Status",
        required=True,
        widget=forms.Select(attrs={
            'class':'form-select',
        })
    )
    
    class Meta:
        model = models.Scholarship
        fields = ['scholarship_name', 'description', 'eligibility', 'deadline', 'grant_officer', 'requirements','status']
        
    def clean_eligibility(self):
        # Clean the input and ensure it's a list of values
        return self.cleaned_data['eligibility']
        
class StudentInformationForm(forms.ModelForm):
    bound_field_class = CustomBoundField
    first_name = forms.CharField(label="First Name", required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    last_name = forms.CharField(label="Last Name", required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    middle_name = forms.CharField(label="Middle Name", required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = models.StudentProfile
        exclude = ['user']
        
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'fathers_contact_no': forms.NumberInput(attrs={'type':'tel'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number', 'type':'tel', 'maxlength': '11',
            'pattern': '[0-9]{11}',}),
            'address': forms.TextInput(attrs={'placeholder':'Enter permanent address'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)

        # Add form-control class to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Set the initial values from user if user exists
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['middle_name'].initial = user.middle_name
            
        self.fields['municipality'].choices = [('', 'Select Municipality')] + [
        (choice.value, choice.label) for choice in models.Residence if choice != models.Residence.ALL]
        
        self.fields['school_enrolled'].choices=[('', 'Select School')] + [
            (choice.value, choice.label) for choice in  models.CamarinesNorteSchool]