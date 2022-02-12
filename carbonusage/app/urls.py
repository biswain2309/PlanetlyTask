from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('api/users/', views.get_post_users, name='get_post_users'),
    path('api/usage/', views.UserUsageList.as_view(), name='per_user_usage'),
    path('api/users/usage/<pk>', views.UserUsageUpdateDelete.as_view(), name='get_delete_update_user_usage'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

