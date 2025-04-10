# Generated by Django 5.1.3 on 2025-04-08 03:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("biblio", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Emprunt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_emprunt", models.DateTimeField(auto_now_add=True)),
                ("date_retour_prevue", models.DateField()),
                ("date_retour_effective", models.DateTimeField(blank=True, null=True)),
                ("rendu", models.BooleanField(default=False)),
                (
                    "utilisateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Livre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("titre", models.CharField(max_length=200)),
                ("auteur", models.CharField(max_length=150)),
                ("isbn", models.CharField(max_length=13, unique=True)),
                ("date_publication", models.DateField(blank=True, null=True)),
                ("nombre_exemplaires", models.PositiveIntegerField(default=1)),
                ("nombre_disponibles", models.PositiveIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_reservation", models.DateTimeField(auto_now_add=True)),
                (
                    "position_file_attente",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("alerte_envoyee", models.BooleanField(default=False)),
                ("date_alerte_envoyee", models.DateTimeField(blank=True, null=True)),
                (
                    "livre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="biblio.livre"
                    ),
                ),
                (
                    "utilisateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["date_reservation"],
                "unique_together": {("livre", "utilisateur")},
            },
        ),
        migrations.DeleteModel(
            name="Produit",
        ),
        migrations.AddField(
            model_name="emprunt",
            name="livre",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="biblio.livre"
            ),
        ),
    ]
