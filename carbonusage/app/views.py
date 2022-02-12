from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django_filters import rest_framework as filters
from .models import User, Usage, UsageTypes
from .serializers import UserSerializer, UsageSerializer
from .filters import UsageFilter



paginator = PageNumberPagination()
paginator.page_size = 4


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def get_post_users(request):
    # get all users
    if request.method == 'GET':
        users = User.objects.all()
        users_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(users_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    # Insert a record for a User
    if request.method == 'POST':
        data = {
            'id': request.data.get('id'),
            'name': request.data.get('name')
        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''--------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_post_user_usage(request):

    if request.method == 'GET':
        users_usage = Usage.objects.all()
        users_usage_page = paginator.paginate_queryset(users_usage, request)
        serializer = UsageSerializer(users_usage_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method == 'POST':
        data = {
            'id': request.data.get('id'),
            'user_id': request.data.get('user_id'),
            'usage_type_id': request.data.get('usage_type_id'),
            'usage_at': request.data.get('usage_at'),
            'amount': request.data.get('amount')
        }
        serializer = UsageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
--------'''


'''@api_view(['GET', 'DELETE', 'PUT'])
# @permission_classes([IsAuthenticated])
def get_delete_update_user_usage(request, pk):
    try:
        user_usage = Usage.objects.get(id=pk)
        print('--->', user_usage.amount)
    except Usage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # get details of single user
    if request.method == 'GET':
        # serializer = UsageSerializer(user_usage)
        # return Response(serializer.data)
        users_usage_page = paginator.paginate_queryset(user_usage, request)
        serializer = UsageSerializer(users_usage_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    # update details of single user
    if request.method == 'PUT':

        users_usage_page = paginator.paginate_queryset(user_usage, request)
        serializer = UsageSerializer(users_usage_page, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return paginator.get_paginated_response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # delete details of single user
    if request.method == 'DELETE':
        user_usage.delete()
        return Response(status.HTTP_200_OK)
'''

class UserUsageList(generics.ListCreateAPIView):
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UsageFilter


class UserUsageUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer

