from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Post
from .serializers import PostSerializer

# Create your views here.
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()
    
    serializer = PostSerializer(posts, many=True)
    
    return JsonResponse(serializer.data, safe=False)