from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Usage
from .serializers import UserSerializer, UsageSerializer
from .filters import UsageFilter



paginator = PageNumberPagination()
paginator.page_size = 2


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users(request):
    # get all users
    if request.method == 'GET':
        users = User.objects.all()
        users_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(users_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_users(request):
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



@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_delete_update_user(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # get details of single user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    # update details of single user
    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # delete details of single user
    if request.method == 'DELETE':
        user.delete()
        return Response(status.HTTP_200_OK)


class UsageList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = UsageFilter
    ordering_fields = ['usage_at']


class ModifyUsageList(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Usage.objects.all()
    serializer_class = UsageSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_each_users_usage(request, userid):
    try:
        user_usage = Usage.objects.filter(user_id=userid).order_by('usage_at')
        users_usage_page = paginator.paginate_queryset(user_usage, request)
        serializer = UsageSerializer(users_usage_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    except Usage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


        
