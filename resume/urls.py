from django.urls import path
from .views import ResumeListView, ResumeImportView, ResumeCreateView, ResumeDetailView, ResumeRenderView, ResumeDownloadView

urlpatterns = [
    path('', ResumeListView.as_view(), name='resume_list'),
    path('import/', ResumeImportView.as_view(), name='import_resume'),
    path('create/', ResumeCreateView.as_view(), name='create_resume'),
    path('<int:id>/', ResumeDetailView.as_view(), name='resume_detail'),
    path('<int:id>/render/', ResumeRenderView.as_view(), name='render_resume'),
    path('<int:id>/download/', ResumeDownloadView.as_view(), name='download_resume'),
]
