from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Resume
import json

# List all resumes (GET)
class ResumeListView(View):
    def get(self, request):
        resumes = list(Resume.objects.values())
        return JsonResponse(resumes, safe=False)

# Import a new resume (POST)
@method_decorator(csrf_exempt, name='dispatch')
class ResumeImportView(View):
    def post(self, request):
        data = json.loads(request.body)
        resume = Resume.objects.create(title=data['title'], content=data['content'])
        return JsonResponse({'id': resume.id, 'message': 'Resume imported successfully'})

# Create a resume page (GET)
class ResumeCreateView(View):
    def get(self, request):
        return HttpResponse('Resume creation page (render an HTML form or provide JSON)')

# View, update, or delete a specific resume
@method_decorator(csrf_exempt, name='dispatch')
class ResumeDetailView(View):
    def get(self, request, id):
        try:
            resume = Resume.objects.get(pk=id)
            return JsonResponse({'title': resume.title, 'content': resume.content})
        except Resume.DoesNotExist:
            return HttpResponseNotFound('Resume not found')

    def patch(self, request, id):
        try:
            resume = Resume.objects.get(pk=id)
            data = json.loads(request.body)
            resume.title = data.get('title', resume.title)
            resume.content = data.get('content', resume.content)
            resume.save()
            return JsonResponse({'message': 'Resume updated successfully'})
        except Resume.DoesNotExist:
            return HttpResponseNotFound('Resume not found')

    def post(self, request, id):
        try:
            resume = Resume.objects.get(pk=id)
            data = json.loads(request.body)
            resume.title = data.get('title', resume.title)
            resume.content = data.get('content', resume.content)
            resume.save()
            return JsonResponse({'message': 'Resume saved successfully'})
        except Resume.DoesNotExist:
            return HttpResponseNotFound('Resume not found')

    def delete(self, request, id):
        try:
            resume = Resume.objects.get(pk=id)
            resume.delete()
            return JsonResponse({'message': 'Resume deleted successfully'})
        except Resume.DoesNotExist:
            return HttpResponseNotFound('Resume not found')

# Render a specific resume (GET)
class ResumeRenderView(View):
    def get(self, request, id):
        try:
            resume = Resume.objects.get(pk=id)
            return HttpResponse(f"<h1>{resume.title}</h1><p>{resume.content}</p>", content_type='text/html')
        except Resume.DoesNotExist:
            return HttpResponseNotFound('Resume not found')

# Download a specific resume (GET)
class ResumeDownloadView(View):
    def get(self, request, id):
        try:
            resume = Resume.objects.get(pk=id)
            response = HttpResponse(resume.content, content_type='application/text')
            response['Content-Disposition'] = f'attachment; filename="{resume.title}.txt"'
            return response
        except Resume.DoesNotExist:
            return HttpResponseNotFound('Resume not found')

