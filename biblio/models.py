from django.db import models
from django.contrib.auth.models import User

class Livre(models.Model):
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True)
    date_publication = models.DateField(null=True, blank=True)
    nombre_exemplaires = models.PositiveIntegerField(default=1)
    nombre_disponibles = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.titre} par {self.auteur}"

class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateTimeField(null=True, blank=True)
    rendu = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utilisateur.username} a emprunté '{self.livre.titre}' le {self.date_emprunt.strftime('%d/%m/%Y')}"

class Reservation(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_reservation = models.DateTimeField(auto_now_add=True)
    # Potentiellement un champ pour la position dans la file d'attente
    position_file_attente = models.PositiveIntegerField(null=True, blank=True)
    alerte_envoyee = models.BooleanField(default=False)
    date_alerte_envoyee = models.DateTimeField(null=True, blank=True)
    est_disponible = models.BooleanField(default=False)  

    class Meta:
        unique_together = ('livre', 'utilisateur') 
        ordering = ['date_reservation'] 

    def __str__(self):
        return f"{self.utilisateur.username} a réservé '{self.livre.titre}' le {self.date_reservation.strftime('%d/%m/%Y')}"