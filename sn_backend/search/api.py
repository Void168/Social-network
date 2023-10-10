from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

@api_view(['POST'])
def search(request):
    data = request.data
    query = data['query']
    
    users = User.objects.filter(name__icontains=query)
    users_serializer = UserSerializer(users, many=True)
    
    return JsonResponse(users_serializer.data, safe=False)