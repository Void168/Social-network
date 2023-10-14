from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializers, ConversationMessageSerializer

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in=list([request.user]))
    serializer = ConversationSerializer(conversations, many=True)
        
    return JsonResponse(serializer.data, safe=False)