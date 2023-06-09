from django.db import models
from django.utils import timezone


# Create your models here.
class Employe(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    SEXE = [
        ("HOMME", "Homme"),
        ("FEMME", "Femme"),
    ]
    sexe = models.CharField(max_length=5, choices=SEXE)
    email = models.EmailField(max_length=254)
    tel = models.CharField(max_length=20)
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    num_rfid = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class EntreeSortie(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='entree_sorties')
    date_event = models.DateField(auto_now_add=True)
    TYPE_EVENT = [
        ("ENTREE", "Entree"),
        ("SORTIE", "Sortie"),
    ]
    type_event = models.CharField(max_length=6, choices=TYPE_EVENT)
    time = models.TimeField(auto_now_add=True)

    def est_aujourd_hui(self):
        return self.date_event == timezone.now().date()


class Presence(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date = models.DateField()
    heure_arv = models.DateTimeField(null=True, blank=True)
    heure_dep = models.DateTimeField(null=True, blank=True)
