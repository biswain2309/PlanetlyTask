from django.urls import path
from . import views


urlpatterns = [
    path('get/users/', views.get_users, name='get_users'),
    path('users/', views.post_users, name='post_users'),
    path('users/<pk>', views.get_delete_update_user, name='get_delete_update_user'),
    path('usages/', views.UsageList.as_view(), name='per_user_usage'),
    path('usage/<pk>', views.ModifyUsageList.as_view(), name='get_delete_update_user_usage'),
    path('users/usage/<userid>', views.get_each_users_usage, name='get_each_user_usage'),
]

