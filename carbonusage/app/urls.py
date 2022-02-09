from django.urls import path
from . import views


urlpatterns = [
    path('api/users/', views.get_post_users, name='get_post_users'),
    path('api/user/usage/<pk>', views.get_delete_update_user_usage, name='get_delete_update_user_usage')
]
