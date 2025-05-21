from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import Role

class LoginRequiredMiddleware:
  
  def __init__(self, get_response):
    self.get_response = get_response
    
  def __call__(self, request):
    excluded_paths = [
			reverse('scholar:landing_page'),
			reverse('scholar:login'),
			reverse('scholar:register'),
      
		]
    
    if (
      not request.user.is_authenticated and
      request.path not in excluded_paths and
      not request.path.startswith('/admin/')
    ):
      messages.error(request, "You must be logged in to view this page.")
      return redirect('scholar:login')
    
    response = self.get_response(request)
    return response

class RoleBasedAccessMiddleware:
  
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
    if request.path.startswith('/administrator/') and request.user.role != Role.ADMIN:
      if request.user.is_authenticated:
        messages.warning(request, "You are attempting to access a restricted area. Unauthorized access to the admin page is prohibited.")
        return redirect('scholar:home')
      else:
        return redirect('scholar:login')
    elif request.path.startswith('/student/') and request.user.role != Role.STUDENT:
      if request.user.is_authenticated:
        messages.warning(request, "You do not have permission to access user accounts.")
        return redirect('scholar:admin-dashboard')
      else:
        return redirect('scholar:login')
        
    response = self.get_response(request)
    return response