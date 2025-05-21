from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    STUDENT = "student", "Student"

class Status(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"
    
class Gender(models.TextChoices):
    EMPTY = "", "-- Select Gender --"
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    CUSTOM = "custom", "Custom"

class CivilStatus(models.TextChoices):
    EMPTY = "", "-- Select Status --"
    SINGLE = "single", "Single"
    MARRIED = "married", "Married"
    WIDOWED = "widowed", "Widowed"

class CamarinesNorteSchool(models.TextChoices):
    CNSC = "camarines norte state college", "Camarines Norte State College"
    OLLCF = "our lady of lourdes college foundation", "Our Lady of Lourdes College Foundation"
    LACO = "la consolacion college of daet, inc.", "La Consolacion College of Daet, Inc."
    MC = "mabini colleges", "Mabini Colleges"
    CNC = "camarines norte college", "Camarines Norte College"
    SFCCA = "st. francis caracciolo culinary academy", "St. Francis Caracciolo Culinary Academy "
    CNSL = "camarines norte school of law", "Camarines Norte School of Law"
class Residence(models.TextChoices):
    ALL = "all", "All"
    BASUD = "basud", "Basud"
    CAPALONGA = "capalonga", "Capalonga"
    DAET = "daet", "Daet"
    JOSE_PANGANIBAN = "jose panganiban", "Jose Panganiban"
    LABO = "labo", "Labo"
    MERCEDES = "mercedes", "Mercedes"
    PARACALE = "paracale", "Paracale"
    SAN_LORENZO = "san lorenzo", "San Lorenzo"
    SAN_VICENTE = "san vicente", "San Vicente"
    SANTA_ELENA = "santa elena", "Santa Elena"
    TALISAY = "talisay", "Talisay"
    VINZONS = "vinzons", "Vinzons"

class ApplicationStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    APPROVED = "Approved", "Approved"
    REJECT = "Reject", "Reject"
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You did not entered a valid email address.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    is_already_filled_form = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def _str_(self):
        return f"{self.first_name} {self.last_name}--- {self.role}"

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    municipality=models.CharField(max_length=100, choices=Residence.choices, default="")
    address = models.CharField(max_length=255, default="")
    gender = models.CharField(max_length=10, choices=Gender.choices, default="")
    civil_status = models.CharField(max_length=20, choices=CivilStatus.choices, default="")
    birth_date = models.DateField(null=True, blank=True)
    school_enrolled = models.CharField(max_length=70, choices=CamarinesNorteSchool.choices, default="")
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    
    fathers_first_name = models.CharField(max_length=100, default="")
    fathers_last_name = models.CharField(max_length=100, default="")
    fathers_middle_name = models.CharField(max_length=100, default="")
    mothers_first_name = models.CharField(max_length=100, default="")
    mothers_last_name = models.CharField(max_length=100, default="")
    mothers_middle_name = models.CharField(max_length=100, default="")
    
    fathers_home_address = models.CharField(max_length=255, default="")
    fathers_contact_no = models.CharField(max_length=11, default="")
    fathers_occupation = models.CharField(max_length=100, default="")
    fathers_citizenship = models.CharField(max_length=100, default="")
    fathers_religion = models.CharField(max_length=50, default="")
    
    mothers_home_address = models.CharField(max_length=255, default="")
    mothers_contact_no = models.CharField(max_length=11, default="")
    mothers_occupation = models.CharField(max_length=100,default="")
    mothers_citizenship = models.CharField(max_length=100, default="")
    mothers_religion = models.CharField(max_length=50, default="")
    
class Scholarship(models.Model):
    scholarship_name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    eligibility = ArrayField(models.CharField(max_length=30, choices=Residence.choices), default=list, blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    requirements = models.TextField(max_length=250, blank=True, null=True)
    grant_officer = models.CharField(max_length=100, default="")
class ScholarshipApplication(models.Model):
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    status= models.CharField(max_length=30, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    remarks = models.TextField(default="")

class ApplicationDocuments(models.Model):
    application = models.ForeignKey(ScholarshipApplication, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)