# ResultChecker/views.py - COMPLETE VERSION
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from googleapiclient.http import MediaIoBaseDownload
import io
import traceback
from django.conf import settings
from django.contrib.auth.decorators import login_required  # ADD THIS IMPORT

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json


@login_required
def general_exam_page(request):
    """Main page for parents to search results"""
    return render(request, "id/general_page.html")




def login_view(request):
    """
    Handle login requests from the portal
    """
    # Check if user is already logged in
    if request.user.is_authenticated:
        return redirect('/')  # Redirect to home page if already logged in
    
    if request.method == 'POST':
        # Check if it's an AJAX request (from mobile)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                data = json.loads(request.body)
                username = data.get('username')
                password = data.get('password')
                
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    login(request, user)
                    return JsonResponse({
                        'success': True,
                        'message': 'Login successful! Welcome to Emilia Foremost High School Portal.',
                        'redirect_url': '/'  # Redirect to home page
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid username or password. Please try again.'
                    })
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid request format.'
                })
        
        # Regular form submission (desktop)
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful! Welcome to Emilia Foremost High School Portal.')
            return redirect('/')  # Redirect to home page
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login_page')
    
    # GET request - show login page
    return render(request, 'id/student_portal.html')

def logout_view(request):
    """
    Handle logout requests
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login_page')
