from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class LoginRequiredMiddleware:
  
  def __init__(self, get_response):
    self.get_response = get_response
    
  def __call__(self, request):
    excluded_paths = [
			reverse('scholar:landing_page'),
			reverse('scholar:login'),
			reverse('scholar:register'),
		]
    
    if not request.user.is_authenticated and request.path not in excluded_paths:
      messages.error(request, "You must be logged in to view this page.")
      return redirect('scholar:login')
    
    response = self.get_response(request)
    return response