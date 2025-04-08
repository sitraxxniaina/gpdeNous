from django.contrib import admin
from .models import Livre, Reservation, Emprunt

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'livre', 'date_reservation')
    list_filter = ('livre', 'utilisateur')

class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('livre', 'utilisateur', 'date_emprunt', 'date_retour_prevue', 'rendu')
    list_filter = ('livre', 'utilisateur', 'rendu')
    date_hierarchy = 'date_emprunt'

admin.site.register(Livre)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Emprunt, EmpruntAdmin) 