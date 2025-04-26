from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from . import models


class StyledLabelBoundField(forms.BoundField):
    def label_tag(self, contents=None, attrs=None, label_suffix=None, tag=None):
        attrs = attrs or {}
        attrs["class"] = "form-label fw-bold mb-0"
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
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2',]

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
    
    bound_field_class = StyledLabelBoundField

    scholarship_name = forms.CharField(
        required=True,
        label="Scholarship Name",
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder': 'Iskolar ng Bayan Program'
        })
    )
    
    description = forms.CharField(
        label="Description:",
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
        fields = ['scholarship_name', 'description', 'eligibility', 'deadline', 'status']
        
    def clean_eligibility(self):
        # Clean the input and ensure it's a list of values
        return self.cleaned_data['eligibility']
        