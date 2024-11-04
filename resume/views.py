from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import models
import json

# List all resumes (GET)
class ResumeListView(View):
    def get(self, request):
        try:
            userID = request.COOKIES['UID']
            resumes = models.fetch_resumes(userID)
        except:
            return HttpResponse('Unauthorized', status=401)
        return JsonResponse(resumes, safe=False)

# Import a new resume (POST)
@method_decorator(csrf_exempt, name='dispatch')
class ResumeImportView(View):
    def post(self, request):
        data = json.loads(request.body)
        resume = models.create_resume(data['userID'], data['title'], data['content'])
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
            resume = models.fetch_resum_by_id(request.COOKIES['UID'], id)
            return JsonResponse({'title': resume.title, 'content': resume.content})
        except:
            return HttpResponseNotFound('Resume not found')

    def patch(self, request, id):
        try:
            data = json.loads(request.body)
            title = data.get('title', resume.title)
            content = data.get('content', resume.content)
            resume = models.update_resume(request.COOKIES['UID'], id, title, content)
            return JsonResponse({'message': 'Resume updated successfully'})
        except:
            return HttpResponseNotFound('Resume not found')

    def post(self, request, id):
        try:
            data = json.loads(request.body)
            title = data.get('title', title)
            content = data.get('content', content)
            resume = models.update_resume(request.COOKIES['UID'], id, title, content)
            return JsonResponse({'message': 'Resume saved successfully'})
        except:
            return HttpResponseNotFound('Resume not found')

    def delete(self, request, id):
        try:
            resume = models.delete_resume(request.COOKIES['UID'], id)
            return JsonResponse({'message': 'Resume deleted successfully'})
        except:
            return HttpResponseNotFound('Resume not found')

# Render a specific resume (GET)
class ResumeRenderView(View):
    def get(self, request, id):
        try:
            resume = models.fetch_resum_by_id(request.COOKIES['UID'], id)
            resume = json.loads(resume)
            return HttpResponse(f"<h1>{resume.title}</h1><p>{resume.content}</p>", content_type='text/html')
        except:
            return HttpResponseNotFound('Resume not found')

# Download a specific resume (GET)
class ResumeDownloadView(View):
    def get(self, request, id):
        try:
            resume = models.fetch_resum_by_id(request.COOKIES['UID'], id)
            response = HttpResponse(json.loads(resume), content_type='application/text')
            response['Content-Disposition'] = f'attachment; filename="{resume.title}.txt"'
            return response
        except:
            return HttpResponseNotFound('Resume not found')

