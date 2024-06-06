from django.contrib import admin
from django.utils.html import format_html
from rt_app.models import Lixeira, Bairro
from django.contrib import admin




class LixeiraAdmin(admin.ModelAdmin):
    list_display = ("localizacao", "tipo_residuo", "mostrar_progresso")
    list_filter = ("tipo_residuo", "status_manutencao")
    search_fields = ("localizacao", "domicilio")


    def mostrar_progresso(self, obj):
        # Define a cor da barra de progresso com base no valor
        progresso = obj.get_progresso()
        cor = "green" if progresso==0.00 else ("yellow" if progresso>50.00 and progresso<100.00 else "red")
        return format_html(
            '<div style="width: 100%; background-color: lightgrey;">'
            f'<div style="width: {progresso}%; background-color: {cor}; text-align: center;">{progresso}%</div>'
            '</div>'
        )

    mostrar_progresso.short_description = "Capacidade Atual"

admin.site.register(Lixeira, LixeiraAdmin)
admin.site.register(Bairro)
