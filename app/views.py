import paho.mqtt.client as mqtt

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import Employe, EntreeSortie

from django.shortcuts import render


# zakaria
def list_employes(request):
    employes = Employe.objects.all()
    return render(request, 'liste_employes.html', {'employes': employes})


def details_employe(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    events = employe.entree_sorties.filter(employe=employe, date_event=timezone.now().date()).order_by("-time")
    num_events = events.count()
    return render(request, 'details_employe.html', {'employe': employe, 'events': events, 'num_events': num_events})


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



def update_employe(request, pk):
    if request.method == 'POST':
        employe = get_object_or_404(Employe, pk=pk)

        #new_num_rfid = request.POST.get('num_rfid')
        new_nom = request.POST.get('nom')
        new_prenom = request.POST.get('prenom')
        new_sexe = request.POST.get('sexe')
        new_email = request.POST.get('email')
        new_tel = request.POST.get('tel')


        #employe.num_rfid = new_num_rfid
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







def delete_employe_view(request, pk):
    employe = get_object_or_404(Employe, pk=pk)
    if request.method == 'POST':
        employe.delete()
        return redirect('list_employes')
    return render(request, 'delete_employe.html', {'employe': employe})


def dashboard(request):
    employes = Employe.objects.all()
    entree_sorties = EntreeSortie.objects.all().order_by('-date_event')[:3]
    events = EntreeSortie.objects.count()
    context1 = {
        'entree_sorties': entree_sorties,'employes': employes, 'events':events
    }
    return render(request, 'dashboard.html', context1)



def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("duess/rfid/dv1/uid")


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
