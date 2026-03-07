import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserEditForm, LoginForm # LoginForm кошулду
from .models import CustomUser, EmailOTP , ContactMessage



# 1. Регистрация
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, "Регистрация ийгиликтүү өттү!")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = RegisterForm()
    return render(request, 'registration/signup.html', {'form': form})

# 2. Кадимки Кирүү (Логин жана Пароль менен)
def login_view(request):
    if request.method == "POST":
        # Сиздин эски LoginForm же стандарттык authenticate колдонобуз
        u_name = request.POST.get('username')
        p_word = request.POST.get('password')
        user = authenticate(username=u_name, password=p_word)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Колдонуучунун аты же пароль туура эмес.")
    
    return render(request, 'registration/login.html')

# 3. Паролду унутуп калганда Email-OTP жөнөтүү
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            EmailOTP.objects.filter(email=email).delete()
            EmailOTP.objects.create(email=email, otp_code=otp)
            
            send_mail(
                'Паролду калыбына келтирүү | Bilim Platform',
                f'Сиздин кирүү кодуңуз: {otp}',
                'noreply@bilim.kg',
                [email],
                fail_silently=False,
            )
            request.session['reset_email'] = email
            return redirect('verify_otp')
        except CustomUser.DoesNotExist:
            messages.error(request, "Бул Email дареги катталган эмес.")
            
    return render(request, 'registration/forgot_password.html')

# 4. OTP Кодду текшерүү жана киргизүү
def verify_otp_view(request):
    email = request.session.get('reset_email')
    if not email:
        return redirect('login')

    if request.method == "POST":
        user_code = request.POST.get('otp_code')
        otp_entry = EmailOTP.objects.filter(email=email, otp_code=user_code).last()

        if otp_entry and otp_entry.is_valid():
            user = CustomUser.objects.get(email=email)
            login(request, user) # Код туура болсо, паролсуз эле киргизебиз
            otp_entry.delete()
            del request.session['reset_email']
            return redirect('/')
        else:
            messages.error(request, "Код туура эмес же мөөнөтү бүттү.")
    
    return render(request, 'registration/verify_otp.html', {'email': email})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профилиңиз жаңыртылды!")
            return redirect('edit_profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'registration/edit_profile.html', {'form': form})
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Базага сактоо
        ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=message
        )

        # Админге (сизге) почтага билдирүү жөнөтүү
        full_message = f"Жаңы билдирүү келди!\n\nКимден: {name}\nEmail: {email}\nТема: {subject}\nКат: {message}"
        send_mail(
            f"Жаңы байланыш: {subject}",
            full_message,
            'ishakishakov00@gmail.com', # Жөнөтүүчү
            ['ishakishakov00@gmail.com'], # Алуучу (өзүңүздүн почтаңызды жазыңыз)
            fail_silently=False,
        )
        messages.success(request, "Сиздин билдирүүңүз ийгиликтүү жөнөтүлдү!")
        return redirect('/')
    
    return render(request, 'registration/contact.html')