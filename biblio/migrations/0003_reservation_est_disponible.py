# Generated by Django 5.1.3 on 2025-04-08 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("biblio", "0002_emprunt_livre_reservation_delete_produit_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="est_disponible",
            field=models.BooleanField(default=False),
        ),
    ]
