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
    ARCHIVED = "archived", "Archived"
    
class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    CUSTOM = "custom", "Custom"

class CivilStatus(models.TextChoices):
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def _str_(self):
        return f"{self.first_name} {self.last_name}--- {self.role}"

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    address = models.CharField(max_length=255, default="")
    gender = models.CharField(max_length=10, choices=Gender.choices, default=Gender.CUSTOM)
    civil_status = models.CharField(max_length=20, choices=CivilStatus.choices, default=CivilStatus.SINGLE)
    birth_date = models.DateField(null=True, blank=True)
    school_enrolled = models.CharField(max_length=70, choices=CamarinesNorteSchool.choices, default="")
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    permanent_address = models.CharField(max_length=255, default="")
    
    fathers_first_name = models.CharField(max_length=100, default="")
    fathers_last_name = models.CharField(max_length=100, default="")
    mothers_first_name = models.CharField(max_length=100, default="")
    mothers_last_name = models.CharField(max_length=100, default="")
    
    guardian = models.CharField(max_length=130, default="")
    rel_in_guardian = models.CharField(max_length=50, default="")
    guardian_address = models.CharField(max_length=255, default="")
    guardian_no = models.CharField(max_length=20, default="")
    
    fathers_home_address = models.CharField(max_length=255, default="")
    fathers_contact_no = models.CharField(max_length=20, default="")
    fathers_occupation = models.CharField(max_length=100, default="")
    fathers_age = models.IntegerField(default=0)
    fathers_birthdate = models.DateField(null=True, blank=True)
    fathers_citizenship = models.CharField(max_length=100, default="")
    fathers_religion = models.CharField(max_length=50, default="")
    
    mothers_home_address = models.CharField(max_length=255, default="")
    mothers_contact_no = models.CharField(max_length=20, default="")
    mothers_occupation = models.CharField(max_length=100,default="")
    mothers_age = models.IntegerField(default=0)
    mothers_birthdate = models.DateField(null=True, blank=True)
    mothers_citizenship = models.CharField(max_length=100, default="")
    mothers_religion = models.CharField(max_length=50, default="")
    
    
    
class StudentInformation(models.Model):
    pass
class Scholarship(models.Model):
    scholarship_name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(blank=True)
    eligibility = ArrayField(models.CharField(max_length=30, choices=Residence.choices), default=list, blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    # requirements = models.TextField(max_length=250, blank=True, null=True)
class ScholarshipApplication(models.Model):
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)
    