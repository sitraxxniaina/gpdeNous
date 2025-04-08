from django.contrib import admin
from django.urls import path, include
from biblio import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('biblio.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', views.profil_utilisateur, name='profil_utilisateur'),
]