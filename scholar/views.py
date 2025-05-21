from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm, ScholarForm, StudentInformationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from . import models
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime
import calendar

def landing_page(request):
    if request.user.is_authenticated:
        if request.user.role == "student":
            return redirect('scholar:home')
        elif request.user.role == "admin":
            return redirect('scholar:admin-dashboard')

    return render(request, "scholar/landing_page.html")

def login_page(request):
    if request.user.is_authenticated:
        if request.user.role == "student":
            return redirect('scholar:home')
        elif request.user.role == "admin":
            return redirect('scholar:admin-dashboard')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == "student":
                if user.is_already_filled_form:
                    return redirect('scholar:home')
                else:
                    return redirect('scholar:information')
            elif user.role == "admin":
                return redirect('scholar:admin-dashboard')
        else:
            messages.error(request, "Invalid username or password")
            print("invalid form")
    else:
        form = UserLoginForm()
    
    return render(request, "scholar/login.html", {"form": form})

def register_page(request):
    
    if request.user.is_authenticated:
        if request.user.role == "student":
            return redirect('scholar:home')
        elif request.user.role == "admin":
            return redirect('scholar:admin-dashboard')

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
    student_profile = request.user.student_profile
    user_municipality = request.user.student_profile.municipality
    current_year = datetime.now().year

    count_open_scholarship = models.Scholarship.objects.filter(
        status="open",
        deadline__gte=timezone.now()
    ).filter(
        Q(eligibility__len=0) | Q(eligibility__contains=[user_municipality])
    ).count()
    
    count_applied_scholarship = models.ScholarshipApplication.objects.filter(
        student=student_profile
    ).count()
    
    count_approved_scholarship = models.ScholarshipApplication.objects.filter(
        student=student_profile,
        status="Approved"
    ).count()

    monthly_data = (
        models.Scholarship.objects
        .filter(created_at__year=current_year)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    monthly_dict = {item['month'].month: item['count'] for item in monthly_data}
    
    labels = [calendar.month_name[m] for m in range(1, 13)]
    datas = [monthly_dict.get(m, 0) for m in range(1, 13)]
    
    status_counts = (
        models.ScholarshipApplication.objects
        .filter(student=student_profile)
        .values('status')
        .annotate(count=Count('id'))
    )
    
    print(status_counts)
    
    status_dict = {item['status']: item['count'] for item in status_counts}
    status_labels = ['Approved', 'Pending', 'Rejected']
    status_data = [
        status_dict.get('Approved', 0),
        status_dict.get('Pending', 0),
        status_dict.get('Reject', 0),
    ]
    
    context = {
        'open_scholarship': count_open_scholarship,
        'applied_scholarshio':count_applied_scholarship,
        'approved_scholarship':count_approved_scholarship,
        'labels':labels,
        'datas':datas,
        'status_labels': status_labels,
        'status_data': status_data
    }
    return render(request, "scholar/student.html", context)

def view_available_scholarship(request):
    if request.user.is_already_filled_form:
        user_municipality = request.user.student_profile.municipality

        scholarships = models.Scholarship.objects.filter(
            status="open",
            deadline__gte=timezone.now()
        ).filter(
            Q(eligibility__len=0) | Q(eligibility__contains=[user_municipality])
        ).order_by('-id')
        return render(request, "scholar/apply_scholarship.html", {'scholarships':scholarships})
    else:
        messages.info(request, "Please complete the remaining fields to view available scholarships.")
        return redirect('scholar:information')

def view_scholarship(request, id):
    student_profile = request.user.student_profile
    scholarship_item = get_object_or_404(models.Scholarship,id=id)
    if request.method == 'POST':
        files = request.FILES.getlist('documents')

        already_applied = models.ScholarshipApplication.objects.filter(
            scholarship=scholarship_item,
            student=student_profile
        ).exists()
        
        if already_applied:
            messages.error(request, "Application failed. You have already submitted an application. Please wait for confirmation.")
        else:
            application = models.ScholarshipApplication.objects.create(
                scholarship=scholarship_item,
                student=student_profile
            )
        
            for f in files:
                models.ApplicationDocuments.objects.create(application=application, file=f)
            messages.success(request, "Application submitted successfully.")
            return redirect('scholar:open-scholarship')
    
    return render(request, "scholar/scholarship.html",{'scholarship':scholarship_item})

def apply_scholarship(request, scholarship_id):
    student_profile = request.user.student_profile
    scholarship = get_object_or_404(models.Scholarship, id=scholarship_id)

    already_applied = models.ScholarshipApplication.objects.filter(
        scholarship=scholarship,
        student=student_profile
    ).exists()
    
    if already_applied:
        messages.error(request, "Application failed. You have already submitted an application. Please wait for confirmation.")
    else:
        models.ScholarshipApplication.objects.create(
            scholarship=scholarship,
            student=student_profile
        )
        
        messages.success(request, "Successfully applied for the scholarship!")
    
    return redirect('scholar:open-scholarship')

def application_status(request):
    student_profile = request.user.student_profile
    applied_scholarship_qs = models.ScholarshipApplication.objects.filter(
        student=student_profile
    ).prefetch_related('documents')
    for app in applied_scholarship_qs:
        print(app.remarks)
        
    applied_scholarship = [
        [app.scholarship.scholarship_name, app.application_date.strftime('%B %d, %Y').replace(' 0', ' '), app.status.capitalize(), app.id]
        for app in applied_scholarship_qs
    ]
    context =  {
        'applied_scholarship':applied_scholarship or [], 
        'applied_scholarship_qs':applied_scholarship_qs
    }
    return render(request, 'scholar/application_status.html',context)

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
    actions = ['close', 'open']
    if action in actions:
        result = models.Scholarship.objects.filter(pk=pk).first()
        scholarship_name = result.scholarship_name
    
        if result:
            if action == "close":
                text = "has been closed successfully."
                result.status = models.Status.CLOSED
            elif action == "open":
                text ="opened successfully."
                result.status = models.Status.OPEN
            
            result.save(update_fields=['status'])
            messages.success(request, f"{scholarship_name} {text}")
    else:
        messages.error(request, "Oops! It looks like you're trying to access something in an unintended way. This action has been blocked for your safety.")
        
    return redirect('scholar:manage-scholarship')

def manage_scholarship_application(request):
    return render(request, "scholar/manage_scholarship_application.html")

def activity_logs(request):
    return render(request, "scholar/activity_logs.html")

def logout_user(request):
    logout(request)
    return redirect('scholar:landing_page')