# -*- coding: utf-8 -*-
from models import *
from forms import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group, Permission

admin.site.unregister(Site)
admin.site.unregister(Group)

def permission_unicode(self):
    return  u'%s' % (self.name,)
Permission.__unicode__ = permission_unicode

class MyUserAdmin(UserAdmin):
    form = CambiarusuarioForm
    add_form = CrearusuarioForm

    list_display = ('usuario', 'email', 'perfil')
    list_filter = ('perfil', )
    
    fieldsets = (
                (None, {'fields': ('usuario', 'email', 'password')}),
                ('Perfil', {'fields': ('perfil',)}),
                ('Permisos', {'fields': ('administrador', 'activo', 'user_permissions')}),
    )
    add_fieldsets = (
                    (None, {'classes': ('wide',), 'fields': ('usuario', 'password1', 'password2',)}),
    )
    search_fields = ('usuario', 'email')
    ordering = ('usuario',)
    filter_horizontal = ('user_permissions',)
    exclude = ['is_superuser']

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'user_permissions':
            query = Permission.objects.filter(content_type__app_label="app")
            kwargs['queryset'] = query
        return super(MyUserAdmin, self).formfield_for_manytomany(db_field, request=request, **kwargs)

class UsuarioAdmin(reversion.VersionAdmin, MyUserAdmin):
    pass

class GraficasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'curso', 'Modificar')
    list_filter = ('curso', )
    search_fields = ('nombre',)


class ValoresAdmin(admin.ModelAdmin):
    list_display = ('id', 'grafica', 'value', 'label',)
    list_filter = ('grafica', )
    search_fields = ('id',)

class ComentariosAdmin(admin.ModelAdmin):
    list_display = ('grafica', 'usuario', 'calificacion', 'comentario' )
    list_filter = ('grafica', 'usuario')
    list_editable = ('calificacion',)
    
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Graficas, GraficasAdmin)
admin.site.register(Curso)
admin.site.register(Valores, ValoresAdmin)
admin.site.register(Comentarios, ComentariosAdmin)






