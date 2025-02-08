from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """ Permissão para Administradores """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permite que qualquer usuário autenticado visualize os dados (GET),
    mas restringe as ações de modificação (POST, PUT, DELETE) apenas para administradores.
    """
    def has_permission(self, request, view):
        # Se for uma requisição de leitura (GET, HEAD, OPTIONS), permite para qualquer usuário autenticado
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Se for uma requisição de modificação, apenas administradores podem
        return request.user.is_authenticated and request.user.role == 'admin'

