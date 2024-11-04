from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from supabase import create_client
import os
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

load_dotenv()

SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        try:
            response = supabase.auth.sign_up({'email': email, 'password': password})
            return HttpResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        try:
            response = supabase.auth.sign_in_with_password({'email': email, 'password': password})
            return HttpResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        try:
            supabase.auth.sign_out()
            return JsonResponse({'message': 'Successfully logged out'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(View):
    def post(self, request):
        email = request.POST['email']

        try:
            response = supabase.auth.reset_password_for_email(email)
            return JsonResponse({'message': 'Password reset email sent.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetView(View):
    def post(self, request):
        access_token = request.POST.get('access_token')
        new_password = request.POST.get('new_password')

        try:
            supabase.auth.set_session(access_token)  

            user = supabase.auth.update_user({'password': new_password}) 
            return JsonResponse({'message': 'Password has been updated successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
