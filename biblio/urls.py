from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('reserver/<int:livre_id>/', views.reserver_livre, name='reserver_livre'),
    path('mes_reservations/', views.mes_reservations, name='mes_reservations'),
    path('emprunter/', views.liste_livres_emprunt, name='liste_livres_emprunt'),
    path('emprunter/<int:livre_id>/', views.emprunter_livre, name='emprunter_livre'),
    path('retourner/', views.liste_emprunts_retour, name='liste_emprunts_retour'),
    path('retourner/<int:emprunt_id>/', views.retourner_livre, name='retourner_livre'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profil_utilisateur, name='profil_utilisateur'),
    path('emprunter/reserve/<int:livre_id>/', views.emprunter_livre_reserve, name='emprunter_livre_reserve'),
    path('annuler_reservation/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'), 
    path('historique_emprunts/', views.historique_emprunts, name='historique_emprunts'),
    path('rechercher/', views.rechercher_livres, name='rechercher_livres'),
]