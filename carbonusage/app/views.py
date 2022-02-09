from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Usage, UsageTypes
from .serializers import UserSerializer, UsageSerializer



@api_view(['GET', 'POST'])
def get_post_users(request):
    # get all users
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
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
def get_delete_update_user_usage(request, pk):
    try:
        user_usage = Usage.objects.get(pk=pk)
    except Usage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # get details of single user
    if request.method == 'GET':
        serializer = UsageSerializer(user_usage, many=True)
        return Response(serializer.data)
    



