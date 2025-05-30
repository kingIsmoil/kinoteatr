from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import RegisterForm, VerificationForm
from .decorators import user_not_authenticated
from .models import CustomUser
import logging

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