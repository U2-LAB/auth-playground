from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import render


def home(request):
    context = {
        'error': '',
        'users': None
    }
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
        else:
            context['error'] = 'Incorrect username or password'
    if not request.session.is_empty():
        users = get_user_model().objects.all()
        context['users'] = users
    return render(request, r'source_of_truth/index.html', context=context)
