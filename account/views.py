from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import RegisterForm, VerificationForm
from .decorators import user_not_authenticated
from .models import CustomUser
import logging
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

logger = logging.getLogger(__name__)

@user_not_authenticated
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                # Создаем пользователя, но не сохраняем
                user = form.save(commit=False)
                # Генерируем код подтверждения
                verification_code = user.generate_verification_code()
                # Теперь сохраняем пользователя
                user.save()
                
                email = form.cleaned_data.get('email')
                
                # Send verification email
                subject = 'Подтверждение регистрации'
                message = f'Ваш код подтверждения: {verification_code}'
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    
                    # В режиме разработки показываем код подтверждения в сообщении
                    if settings.DEBUG:
                        messages.info(request, f'Код подтверждения (только для разработки): {verification_code}')
                    
                except Exception as e:
                    logger.error(f"Ошибка отправки email: {str(e)}")
                    messages.error(request, f'Код подтверждения: {verification_code}')
                
                # Save user ID in session for verification
                request.session['registration_user_id'] = user.id
                messages.success(request, 'Код подтверждения отправлен на ваш email.')
                return redirect('verify_email')
            except Exception as e:
                logger.error(f"Общая ошибка при регистрации: {str(e)}")
                messages.error(request, f'Произошла ошибка при регистрации: {str(e)}')
                return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'cinema/register.html', {'form': form})

@user_not_authenticated
def verify_email(request):
    user_id = request.session.get('registration_user_id')
    if not user_id:
        messages.error(request, 'Сначала необходимо зарегистрироваться.')
        return redirect('register')
    
    try:
        user = CustomUser.objects.get(id=user_id)
        if not user.verification_code:
            # Если код подтверждения отсутствует, генерируем новый
            verification_code = user.generate_verification_code()
            user.save()
        
        if settings.DEBUG:
            messages.info(request, f'Текущий код подтверждения (только для разработки): {user.verification_code}')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Пользователь не найден.')
        return redirect('register')
    
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['verification_code']
            if code == user.verification_code:
                user.is_active = True
                user.verification_code = None
                user.save()
                login(request, user)
                del request.session['registration_user_id']
                messages.success(request, 'Регистрация успешно завершена!')
                return redirect('movie_list')
            else:
                messages.error(request, 'Неверный код подтверждения')
    else:
        form = VerificationForm()
    
    return render(request, 'cinema/verify_email.html', {'form': form})

def logoutview(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(
                    reverse('reset_password', kwargs={'uidb64': uid, 'token': token})
                )
                
                send_mail(
                    'Сброс пароля',
                    f'Для сброса пароля перейдите по ссылке: {reset_url}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Инструкции по сбросу пароля отправлены на ваш email')
                return redirect('login')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Пользователь с таким email не найден')
    else:
        form = PasswordResetForm()
    return render(request, 'cinema/forgot_password.html', {'form': form})

def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Ваш пароль был успешно изменен')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'cinema/reset_password.html', {'form': form})
    else:
        messages.error(request, 'Ссылка для сброса пароля недействительна')
        return redirect('login')