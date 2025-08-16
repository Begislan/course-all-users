from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.views.decorators.csrf import csrf_exempt

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Можно сразу активировать
            user.save()
            messages.success(request, "Регистрация прошла успешно! Теперь войдите.")
            return redirect('login')
        else:
            messages.error(request, "Проверьте правильность данных.")
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Неверный логин или пароль.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')
