from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # EXAMPLES FROM PREV PROJECT
    # path('new', views.addNewUserForm, name='new'),
    # path('handleNewUserForm', views.handleNewUserForm),
    # path('create', views.createCourseForm, name='create'),
    # path('handleCreateCourseForm', views.handleCreateCourseForm),
    # path('join', views.joinCourseForm,name='joinCourseForm'),
    # path('handleJoinCourseForm', views.handleJoinCourseForm, name='handleJoinCourseForm'),
    # path('attendance', views.displayQRCode, name='displayQRCode'),
    # path('upload', views.uploadForm, name='uploadForm'),
    # path('handleUploadForm', views.handleUploadForm, name='handleUploadForm'),
    # path('overview', views.displayCourseOverview, name='displayCourseOverview'),
    # path('student', views.displayCourseStudent, name='displayCourseStudent')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)