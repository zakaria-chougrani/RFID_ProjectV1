# Generated by Django 4.2.1 on 2023-05-13 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('sexe', models.CharField(choices=[('HOMME', 'Homme'), ('FEMME', 'Femme')], max_length=5)),
                ('email', models.EmailField(max_length=254)),
                ('tel', models.CharField(max_length=20)),
                ('date_enregistrement', models.DateTimeField(auto_now_add=True)),
                ('num_rfid', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('heure_arv', models.DateTimeField(blank=True, null=True)),
                ('heure_dep', models.DateTimeField(blank=True, null=True)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employe')),
            ],
        ),
        migrations.CreateModel(
            name='EntreeSortie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_event', models.DateField(auto_now_add=True)),
                ('type_event', models.CharField(choices=[('ENTREE', 'Entree'), ('SORTIE', 'Sortie')], max_length=6)),
                ('time', models.TimeField(auto_now_add=True)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.employe')),
            ],
        ),
    ]