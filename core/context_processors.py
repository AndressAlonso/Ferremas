from .models import PerfilUsuario

def cargar_perfil_y_perfiles(request):
    perfil = None
    perfiles = []

    if request.user.is_authenticated:
        perfil = PerfilUsuario.objects.filter(user=request.user).first()
        perfiles = PerfilUsuario.objects.all()

    return {
        'perfil': perfil,
        'perfiles': perfiles,
    }
