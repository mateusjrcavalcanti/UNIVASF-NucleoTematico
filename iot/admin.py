import functools
from django.contrib import admin
from django import forms
from iot.models import Sensor


class SensorForm(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = ('description', 'token', 'user')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SensorForm, self).__init__(*args, **kwargs)

        if user and self.fields:
            self.fields['user'].initial = user
            if not user.is_superuser:
                self.fields['user'].disabled = True


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    fieldsets = (("Sensor", {'fields': ("description", "token", "user")}),)

    form = SensorForm

    def get_form(self, request, obj=None, **kwargs):
        Form = super().get_form(request, obj, **kwargs)
        return functools.partial(Form, user=request.user)

    def has_change_permission(self, request, obj=None):
        if (not request.user.is_superuser and not request.POST.get('user') is None):
            return True
        return False

    def save_model(self, request, obj, form, change):
        # Verifique se o usuário logado é um superadmin
        if not request.user.is_superuser:
            # Se não for, substitua o campo 'user' pelo usuário logado
            obj.user = request.user

        super().save_model(request, obj, form, change)
