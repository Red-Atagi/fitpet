from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.display_home_page, name='home'),
    path('shop/', views.shop_page, name='shop_page'),
    path('dress/', views.display_dress_page, name='dress_page'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dress/update_clothing/', views.update_clothing, name='update_clothing'),
    path('api/buyclothing/', views.buy_clothing, name='buy_clothing'),
    path('workout/',views.workout_page, name = 'workout_page'),
    path('workout_logged/',views.log_workout, name = 'workout_logged'),
    path('register', views.register, name='register'),
    path('friends/list/', views.friend_list, name='friend_list'),
    path('friends/visit/<int:friend_id>/', views.visit_friend, name='visit_friend'),
    path('friends/requests/', views.friend_request, name="friend_request"),
    path('search_users/', views.search_users, name='search_users'),
    path('send_request/<int:to_user_id>/', views.send_friend_request, name='send_friend_request'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)