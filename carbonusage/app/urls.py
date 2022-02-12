from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('users/', views.get_post_users, name='get_post_users'),
    path('users/<pk>', views.get_delete_update_user, name='get_delete_update_user'),
    path('usages/', views.UsageList.as_view(), name='per_user_usage'),
    path('usage/<pk>', views.ModifyUsageList.as_view(), name='get_delete_update_user_usage'),
    path('users/usage/<userid>', views.get_each_users_usage, name='get_each_user_usage'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]

