from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, QueryDict
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from . import models
from . import mdConvert
import json

# List all resumes (GET)

@method_decorator(csrf_exempt, name='dispatch')
class ResumeListView(View):
    def get(self, request):
        try:
            userID = request.COOKIES['UID']
            resumes = models.fetch_resumes(userID)
        except:
            return HttpResponse('Unauthorized', status=401)
        return HttpResponse(resumes)
    
    def post(self, request):
        # try:
        userID = request.COOKIES['UID']
        resumes = models.create_resume(userID, 'New Resume')
        # except:
        #     return HttpResponse('Unauthorized ', status=401)
        return redirect(f'/resume/{resumes.data[0]["id"]}')

## FIX LATER: BAD CODE: NOT WORKING
# Import a new resume (POST)
@method_decorator(csrf_exempt, name='dispatch')
class ResumeImportView(View):
    def post(self, request):
        data = json.loads(request.body)
        resume = models.create_resume(data['userID'], data['title'], data['content'])
        return JsonResponse({'id': resume.id, 'message': 'Resume imported successfully'})

# Create a resume page (GET)

@method_decorator(csrf_exempt, name='dispatch')
class ResumeCreateView(View):
    def post(self, request):
        resume = models.create_resume(request.COOKIES['UID'], 'New Resume')
        return HttpResponse('Resume creation page (render an HTML form or provide JSON)')

# View, update, or delete a specific resume
@method_decorator(csrf_exempt, name='dispatch')
class ResumeDetailView(View):
    def get(self, request, id):
        try:
            resume = models.fetch_resum_by_id(request.COOKIES['UID'], id)
            return JsonResponse({'title': resume.data[0]['title'], 'content': resume.data[0]['content']})
        except:
            resume = models.fetch_resum_by_id(request.COOKIES['UID'], id)
            # return JsonResponse({'title': resume['data']['title'], 'content': resume['data']['content']})
            return HttpResponseNotFound('Resume not found')

    def post(self, request, id):
        try:
            data = request.POST
            title = data['title']
            content = data['content']
            resume = models.update_resume(request.COOKIES['UID'], id, title, content)
            return JsonResponse({'message': 'Resume saved successfully'})
        except Exception as e:
            return HttpResponseNotFound('Resume not found {}'.format(e))

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
            resume = resume.data[0]
            template = resume['template']
            if template is None or template < 1:
                template = 1
            print(type(template))
            templateStyles = models.getTemplate(template)
            styleText = templateStyles.data[0]['styles']
            print(styleText)
            htmlResume = mdConvert.convertToHTML(resume['content'], styleText)
            return HttpResponse(htmlResume, content_type='text/html')
        except Exception as e: 
            return HttpResponseNotFound('Resume not found {}'.format(e))

# Download a specific resume (GET)
class ResumeDownloadView(View):
    def get(self, request, id):
        try:
            resume = models.fetch_resum_by_id(request.COOKIES['UID'], id)
            ### FIX TO PDF FORMATTER LATER
            # if request.GET.get('format') == 'pdf':
            #     pdfDoc = mdConvert.convertToPDF(mdConvert.convertToHTML(resume.data[0]['content']))
            #     response = HttpResponse(pdfDoc, content_type='application/pdf')
            #     response['Content-Disposition'] = f'attachment; filename="{resume.data[0]["title"]}.pdf"'
            #     return response
            # else:
            response = HttpResponse((resume.data[0]['content']), content_type='application/text')
            response['Content-Disposition'] = f'attachment; filename="{resume.data[0]['title']}.md"'
            return response
        except Exception as e:
            return HttpResponseNotFound('Resume not found, {}'.format(e))

