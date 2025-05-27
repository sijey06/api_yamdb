from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings

from .models import UserProfile
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .serializers import UserProfileSerializer


@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    username = request.data.get('username')

    if not email or not username:
        return Response(
            {'error': 'Email и username обязательны'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = UserProfile.objects.create_user(username=username, email=email)
    user.set_confirmation_code()

    subject = 'Подтверждение регистрации на сайте YAMDB'
    message = f'''Ваш код подтверждения: {user.confirmation_code}'''
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )

    return Response(
        {'confirmation_code': user.confirmation_code},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def confirm_and_get_token(request):
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')

    try:
        user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'Пользователь не найден'},
            status=status.HTTP_404_NOT_FOUND
        )

    if user.confirmation_code != confirmation_code:
        return Response(
            {'error': 'Неверный confirmation code'},
            status=status.HTTP_400_BAD_REQUEST
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }, status=status.HTTP_200_OK)


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'create', 'destroy']:
            return [IsAdminOrReadOnly()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]
