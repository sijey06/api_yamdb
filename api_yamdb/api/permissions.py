from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение только для администратора."""

    def has_permission(self, request, view):
        """Проверяет, что аутентифицированный пользователь - администратор."""
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(IsAdmin):
    """Разрешение на чтение для всех, полные права для администратора."""

    def has_permission(self, request, view):
        """
        Проверяет, что запрошен безопасный метод или аутентифицированный
        пользователь - администратор.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение на чтение для всех, полные права для автора, администратора,
    модератора.
    """

    def has_permission(self, request, view):
        """
        Проверяет, что запрошен безопасный метод или аутентифицированный
        пользователь - автор, администратор, модератор.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Проверяет права доступа к конкретному объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
