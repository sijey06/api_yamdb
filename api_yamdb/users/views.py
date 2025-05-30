from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import DEFAULT_FROM_EMAIL
from api.permissions import IsAdmin
from .models import UserProfile
from .serializers import (TokenSerializer, UserProfileCreateSerializer,
                          UserProfileEditSerializer, UserProfileSerializer)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup(request):
    """Регистрация пользователя."""
    serializer = UserProfileCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    try:
        UserProfile.objects.get(email=email, username=username)
        return Response(
            {'detail': 'Учетная запись уже существует'},
            status=status.HTTP_200_OK
        )
    except UserProfile.DoesNotExist:
        pass

    if UserProfile.objects.filter(email=email).exists():
        return Response(
            {'email': ['Email уже используется']},
            status=status.HTTP_400_BAD_REQUEST
        )

    if UserProfile.objects.filter(username=username).exists():
        return Response(
            {'username': ['Имя пользователя уже занято']},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = UserProfile.objects.create_user(username=username, email=email)
    user.set_confirmation_code()

    send_mail(
        'Код подтверждения YaMDb',
        f'Код подтверждения: {user.confirmation_code}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Получение токена после подтверждения кода."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = get_object_or_404(
        UserProfile,
        username=serializer.validated_data['username']
    )
    conf_code = serializer.validated_data['confirmation_code']
    if user.confirmation_code != conf_code:
        return Response(
            {'confirmation_code': ['Неверный код']},
            status=status.HTTP_400_BAD_REQUEST
        )

    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserProfileViewSet(ModelViewSet):
    """Работа с моделью UserProfile."""

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
            detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        """Информация о текущем залогиненном пользователе."""
        if request.method == 'PATCH':
            serializer = UserProfileEditSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
