from django.contrib import admin
from .models import Employe, EntreeSortie, Presence


# Personnalisation de l'interface d'administration pour le modèle Employe
class EmployeAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "num_rfid")
    search_fields = ("nom", "prenom", "num_rfid")


# Personnalisation de l'interface d'administration pour le modèle EntreeSortie
class EntreeSortieAdmin(admin.ModelAdmin):
    list_display = ("employe", "date_event", "type_event")
    list_filter = ("type_event",)
    search_fields = ("employe__nom", "employe__prenom", "employe__num_rfid")


# Personnalisation de l'interface d'administration pour le modèle Presence
class PresenceAdmin(admin.ModelAdmin):
    list_display = ("employe", "date", "heure_arv", "heure_dep")
    list_filter = ("date",)
    search_fields = ("employe__nom", "employe__prenom", "employe__num_rfid")


# Enregistrer les modèles personnalisés dans l'interface d'administration
admin.site.register(Employe, EmployeAdmin)
admin.site.register(EntreeSortie, EntreeSortieAdmin)
admin.site.register(Presence, PresenceAdmin)
