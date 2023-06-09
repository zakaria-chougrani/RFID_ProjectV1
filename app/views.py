from datetime import datetime
from datetime import timedelta

import paho.mqtt.client as mqtt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Employe, EntreeSortie
from .scheduler import schedule_email, start_scheduler


@login_required(login_url='acces')
def list_employes(request):
    employes = Employe.objects.all()
    return render(request, 'liste_employes.html', {'employes': employes})
@login_required(login_url='acces')
def details_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    events = employe.entree_sorties.filter(employe=employe, date_event=datetime.now().date()).order_by("-time")
    num_events = events.count()
    return render(request, 'details_employe.html', {'employe': employe, 'events': events, 'num_events': num_events})
@login_required(login_url='acces')
@csrf_exempt
def lecture_rfid(request):
    if request.method == 'POST':
        num_rfid = request.POST.get('num_rfid', '')

        try:
            employe = Employe.objects.get(num_rfid=num_rfid)
            employe_data = {
                'nom': employe.nom,
                'prenom': employe.prenom,
                'sexe': employe.sexe,
                'email': employe.email,
                'tel': employe.tel,
                'num_rfid': employe.num_rfid,
                'date_enregistrement': employe.date_enregistrement,
            }
            return JsonResponse({'success': True, 'employe': employe_data})
        except Employe.DoesNotExist:
            return JsonResponse({'success': False})

    return render(request, 'lecture_rfid.html')



@login_required(login_url='acces')
@csrf_exempt
def add_employe(request):
    if request.method == 'POST':
        num_rfid = request.POST.get('num_rfid')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        email = request.POST.get('email')
        tel = request.POST.get('tel')

        employe_existe = Employe.objects.filter(num_rfid=num_rfid).exists()
        employe = Employe(num_rfid=num_rfid, nom=nom, prenom=prenom, sexe=sexe, email=email, tel=tel)

        if employe_existe:
            message = "Cet employé existe déjà."
            return render(
                request,
                'add_empl.html',
                {"message": message},
            )

        else:
            employe.save()
            return redirect('list_employes')
    else:
        return render(request, 'add_empl.html')

@login_required(login_url='acces')
def update_employe(request, pk):
    if request.method == 'POST':
        employe = get_object_or_404(Employe, pk=pk)

        # new_num_rfid = request.POST.get('num_rfid')
        new_nom = request.POST.get('nom')
        new_prenom = request.POST.get('prenom')
        new_sexe = request.POST.get('sexe')
        new_email = request.POST.get('email')
        new_tel = request.POST.get('tel')

        # employe.num_rfid = new_num_rfid
        employe.nom = new_nom
        employe.prenom = new_prenom
        employe.sexe = new_sexe
        employe.email = new_email
        employe.tel = new_tel

        employe.save()
        return render(request, 'update_employe.html', {'employe': employe})
    else:
        employe = get_object_or_404(Employe, pk=pk)
        return render(request, 'update_employe.html', {'employe': employe})

@login_required(login_url='acces')
def delete_employe_view(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.delete()
        return redirect('list_employes')
    return render(request, 'delete_employe.html', {'employe': employe})

@login_required(login_url='acces')
def dashboard(request):
    current_date = datetime.now()
    employee_count = Employe.objects.count()
    entry_exits = EntreeSortie.objects.filter(date_event=current_date).values('employe').distinct()
    report = []
    employee_count_p = 0  # Compteur pour les employés présents
    employee_count_a = 0  # Compteur pour les employés absents

    for entry_exit in entry_exits:
        employe_id = entry_exit['employe']
        employe = Employe.objects.get(pk=employe_id)
        first_entry = EntreeSortie.objects.filter(employe=employe, date_event=current_date, type_event='ENTREE').order_by('time').first()
        last_exit = EntreeSortie.objects.filter(employe=employe, date_event=current_date, type_event='SORTIE').order_by('-time').first()
        history_events = EntreeSortie.objects.filter(employe=employe, date_event=current_date)

        total_work_duration = timedelta()  # Réinitialisation de la durée de travail pour chaque employé
        duration_formatted = ""  # Réinitialisation du format de la durée pour chaque employé

        for i in range(0, len(history_events), 2):
            entry = history_events[i]
            exit_ = history_events[i + 1] if i + 1 < len(history_events) else None

            time_entry = datetime.combine(datetime.today().date(), entry.time)

            if exit_:
                time_exit = datetime.combine(datetime.today().date(), exit_.time)

                time_difference = time_exit - time_entry
                total_work_duration += time_difference
                total_duration = timedelta(seconds=total_work_duration.total_seconds())

                total_seconds = total_duration.total_seconds()

                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                duration_formatted = f"{hours:.0f}h {minutes:.0f}min {seconds:.0f}s"
            else:
                exit_ = None

        if entry:
            employee_count_p += 1
            employee_count_a = employee_count - employee_count_p
        if exit_:
            employee_count_p -= 1
            employee_count_a = employee_count - employee_count_p


        report.append({
            'Employe_nom': employe.nom,
            'Employe_prenom': employe.prenom,
            'premier_entre': first_entry.time if first_entry else 'No entry recorded',
            'dernier_sortie': last_exit.time if last_exit else 'No exit recorded',
            'total_work_duration': f'{duration_formatted}'
        })

    context = {
        'report': report,
        'employee_count_p': employee_count_p,
        'employee_count_a': employee_count_a,
        'employee_count': employee_count
    }
    return render(request, 'dashboard.html', context)



def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("duess/rfid/dv1/uidz")


def on_message(client, userdata, msg):
    num_rfid = msg.payload.decode('utf-8')
    print(num_rfid)
    try:
        employee = Employe.objects.get(num_rfid=num_rfid)
    except Employe.DoesNotExist:
        # No employee found with the given RFID number, do nothing
        return
    if employee.entree_sorties.exists():
        # Get the most recent EntrySortie record for this employee
        last_entry_exit = employee.entree_sorties.latest('id')
        # Determine the type of event based on the last record
        if last_entry_exit.type_event == 'ENTREE':
            type_event = 'SORTIE'  # Last event was an exit, so this is an entry
        else:
            type_event = 'ENTREE'  # Last event was an entry, so this is an exit
    else:
        # No existing records, so this is the first event for this employee
        type_event = 'ENTREE'
    print(type_event)
    EntreeSortie.objects.create(
        employe=employee,
        type_event=type_event
    )


def connect_to_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_start()
start_scheduler()