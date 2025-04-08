from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Livre, Reservation, Emprunt
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.db.models import Q
from .utils import envoyer_email_disponibilite_reservation  

def accueil(request):
    livres = Livre.objects.all()
    context = {'livres': livres}
    return render(request, 'biblio/accueil.html', context)

@login_required
def reserver_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    if request.method == 'POST':
        with transaction.atomic():
            if Reservation.objects.filter(livre=livre, utilisateur=request.user).exists():
                messages.error(request, "Vous avez déjà réservé ce livre.")
                return redirect('accueil')
            else:
                Reservation.objects.create(livre=livre, utilisateur=request.user, date_reservation=timezone.now())
                if livre.nombre_disponibles > 0:
                    livre.nombre_disponibles -= 1
                    messages.success(request, f"Vous avez réservé '{livre.titre}'.")
                else:
                    messages.info(request, f"'{livre.titre}' n'est pas disponible. Votre réservation a été placée en file d'attente.")
                livre.save()
                return redirect('mes_reservations')
    return redirect('accueil')

@login_required
def mes_reservations(request):
    reservations = Reservation.objects.filter(utilisateur=request.user).order_by('date_reservation')
    context = {'reservations': reservations}
    return render(request, 'biblio/mes_reservations.html', context)

class EmpruntForm(forms.Form):
    utilisateur = forms.ModelChoiceField(queryset=User.objects.all(), label="Étudiant/Enseignant")
    date_retour_prevue = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Date de retour prévue")

@permission_required('biblio.add_emprunt')
def liste_livres_emprunt(request):
    livres = Livre.objects.filter(nombre_disponibles__gt=0)
    return render(request, 'biblio/liste_livres_emprunt.html', {'livres': livres})

@permission_required('biblio.add_emprunt')
def emprunter_livre(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    if request.method == 'POST':
        form = EmpruntForm(request.POST)
        if form.is_valid():
            utilisateur = form.cleaned_data['utilisateur']
            date_retour_prevue = form.cleaned_data['date_retour_prevue']
            Emprunt.objects.create(livre=livre, utilisateur=utilisateur, date_emprunt=timezone.now(), date_retour_prevue=date_retour_prevue)
            livre.nombre_disponibles -= 1
            livre.save()
            return redirect('liste_emprunts_retour')
    else:
        form = EmpruntForm()
    return render(request, 'biblio/emprunter_livre.html', {'form': form, 'livre': livre})

@permission_required('biblio.change_emprunt')
def liste_emprunts_retour(request):
    emprunts = Emprunt.objects.filter(rendu=False).order_by('date_retour_prevue')
    return render(request, 'biblio/liste_emprunts_retour.html', {'emprunts': emprunts})

@permission_required('biblio.change_emprunt')
def retourner_livre(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)
    if not emprunt.rendu:
        with transaction.atomic():
            emprunt.rendu = True
            emprunt.date_retour_effective = timezone.now()
            livre = emprunt.livre
            livre.nombre_disponibles += 1
            livre.save()
            emprunt.save()

            # file d'attente
            reservations_en_attente = Reservation.objects.filter(livre=livre, est_disponible=False).order_by('date_reservation')
            if reservations_en_attente.exists():
                premiere_reservation = reservations_en_attente.first()
                premiere_reservation.est_disponible = True
                premiere_reservation.save()
                messages.info(request, f"Le livre '{livre.titre}' est disponible pour {premiere_reservation.utilisateur.username}.")
                # Envoyer l'e-mail de notification
                envoyer_email_disponibilite_reservation(premiere_reservation)

    return redirect('liste_emprunts_retour')

@login_required
def emprunter_livre_reserve(request, livre_id):
    livre = get_object_or_404(Livre, id=livre_id)
    try:
        reservation = Reservation.objects.get(livre=livre, utilisateur=request.user, est_disponible=True)
        with transaction.atomic():
            if livre.nombre_disponibles > 0:
                Emprunt.objects.create(livre=livre, utilisateur=request.user, date_emprunt=timezone.now(), date_retour_prevue=timezone.now() + timezone.timedelta(days=14))
                livre.nombre_disponibles -= 1
                livre.save()
                reservation.delete()
                messages.success(request, f"Vous avez emprunté '{livre.titre}'.")
                return redirect('mes_reservations')
            else:
                messages.error(request, f"Le livre '{livre.titre}' n'est plus disponible pour l'emprunt.")
                return redirect('mes_reservations')
    except Reservation.DoesNotExist:
        messages.error(request, "Cette réservation n'est plus valide ou n'existe pas.")
        return redirect('mes_reservations')

@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, utilisateur=request.user)
    if request.method == 'POST':
        with transaction.atomic():
            livre = reservation.livre
            livre.nombre_disponibles += 1
            livre.save()
            reservation.delete()
            messages.success(request, f"Votre réservation pour '{livre.titre}' a été annulée.")
            return redirect('mes_reservations')
    else:
        messages.error(request, "Méthode non autorisée.")
        return redirect('mes_reservations')

@login_required
def historique_emprunts(request):
    emprunts_passes = Emprunt.objects.filter(utilisateur=request.user, rendu=True).order_by('-date_retour_effective')
    context = {'emprunts_passes': emprunts_passes}
    return render(request, 'biblio/historique_emprunts.html', context)

@login_required
def profil_utilisateur(request):
    emprunts = Emprunt.objects.filter(utilisateur=request.user, rendu=False).order_by('date_emprunt')
    print(emprunts)
    context = {'emprunts': emprunts}
    return render(request, 'biblio/profil_utilisateur.html', context)

def rechercher_livres(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Livre.objects.filter(
            Q(titre__icontains=query) | Q(auteur__icontains=query) | Q(isbn__icontains=query)
        )

    context = {'results': results, 'query': query}
    return render(request, 'biblio/recherche_livres.html', context)