from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegistrationForm, ScholarForm, StudentInformationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from . import models
from django.contrib.auth.decorators import login_required

# Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        if request.user.role == "student":
            return redirect('scholar:home')
        elif request.user.role == "admin":
            return redirect('scholar:admin-dashboard')

    return render(request, "scholar/landing_page.html")

def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == "student":
                return redirect('scholar:home')
            elif user.role == "admin":
                return redirect('scholar:admin-dashboard')
        else:
            print("invalid form")
    else:
        form = UserLoginForm()
    
    return render(request, "scholar/login.html", {"form": form})

def register_page(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()

            if user.role == "student":
                models.StudentProfile.objects.create(user=user)

            messages.success(request, "Registered Succesfully.")
            return redirect("scholar:login")
    else:
        form = UserRegistrationForm
    return render(request, "scholar/register.html", {"form":form})

def logged_in_home(request):
    print(request.user.role)
    return render(request, "scholar/student.html")

def apply_scholarship(request):
    scholarships = models.Scholarship.objects.filter(status="open").order_by('-id')
    return render(request, "scholar/apply_scholarship.html", {'scholarships':scholarships})

def profile(request):
    return render(request, "scholar/profile.html")

def information(request):
    instance = get_object_or_404(models.StudentProfile, user=request.user)
    if request.method == 'POST':
        form = StudentInformationForm(request.POST,  instance=instance)
        user = request.user
        if form.is_valid():
            form.save()
            user.is_already_filled_form = True
            user.save()
            messages.success(request, "Information succesfully updated.")
            return redirect('scholar:information')
        else:
            print(form.errors)
    else:
        form = StudentInformationForm(instance=instance, user=request.user)
    return render(request, "scholar/information.html", {'form':form})

def admin_dashboard(request):
    return render(request, "scholar/admin_dashboard.html")

def admin_manage_scholarship(request):
    scholarships = models.Scholarship.objects.filter(status="open").order_by('-id')
    closed_scholarships = models.Scholarship.objects.filter(status="closed")
    archived_scholarships = models.Scholarship.objects.filter(status="archived")
    scholarship_forms = [ScholarForm(instance=s) for s in scholarships]
    
    if request.method == 'POST':
        form = ScholarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Created Succesfully.")
            return redirect('scholar:manage-scholarship')
        else:
            print(form.errors)

    else:
        form = ScholarForm()
    
    context = {
        'scholarships':scholarships, 
        'closed_scholarships':closed_scholarships, 
        'archived_scholarships':archived_scholarships,
        'form':form,
        'scholarship_forms': zip(scholarships, scholarship_forms)
        }
    return render(request, "scholar/manage_scholarship.html", context)

def update_scholarship(request, pk):
    scholarship = get_object_or_404(models.Scholarship, pk=pk)
    scholarship_name = scholarship.scholarship_name
    if request.method == 'POST':
        form = ScholarForm(request.POST, instance=scholarship) 
        if form.is_valid():
            form.save()
            messages.success(request, f"{scholarship_name} Updated Succesfully!")
            return redirect('scholar:manage-scholarship')
        
def update_scholarship_status(request, pk, action):
    result = models.Scholarship.objects.filter(pk=pk).first()
    scholarship_name = result.scholarship_name
    text = "has been archieved succesfully." if action == 'archive' else "has been closed succesfully."
    if result:
        result.status = models.Status.ARCHIVED if action == 'archive' else models.Status.CLOSED
        result.save(update_fields=['status'])
        messages.success(request, f"{scholarship_name} {text}")
        
    return redirect('scholar:manage-scholarship')

def admin_manage_user(request):
    return render(request, "scholar/manage_user.html")

def activity_logs(request):
    return render(request, "scholar/activity_logs.html")

def logout_user(request):
    logout(request)
    return redirect('scholar:landing_page')