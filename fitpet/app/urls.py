from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop_page, name='shop_page'),
    path('dress/', views.display_dress_page, name='dress'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dress/change_clothing/', views.change_clothing, name='change_clothing')
    # path('register/', views.register, name='register'),
    # path('workout/', views.workout, name='workout_page'),
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