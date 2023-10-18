from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render

from .models import User
# Create your views here.

def activate_email(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')
    
    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()
        
        return render(request, 'ActivatePage.html', {
            'user': user
        })
        
    else:
        return HttpResponse('Có gì đó sai, hãy thử tạo lại tài khoản mới')