import os

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from django.core.mail import send_mail

from app.models import EntreeSortie, Employe


def schedule_email():
    current_time = datetime.now().time()
    if current_time.hour == 20 and current_time.minute == 00:
        # Todo: add rapport
        print("this function runs every 10 seconds")
        global duration_formatted
        current_date = datetime.now()

        entry_exits = EntreeSortie.objects.filter(date_event=current_date).values('employe').distinct()
        report = []
        total_work_duration = timedelta()

        for entry_exit in entry_exits:
            employe_id = entry_exit['employe']
            employe = Employe.objects.get(pk=employe_id)
            first_entry = EntreeSortie.objects.filter(employe=employe, date_event=current_date,
                                                      type_event='ENTREE').order_by('time').first()
            last_exit = EntreeSortie.objects.filter(employe=employe, date_event=current_date,
                                                    type_event='SORTIE').order_by(
                '-time').first()
            history_events = EntreeSortie.objects.filter(employe=employe, date_event=current_date)

            for i in range(0, len(history_events), 2):
                entry = history_events[i]
                exit_ = history_events[i + 1]
                time_entry = datetime.combine(datetime.today().date(), entry.time)
                time_exit = datetime.combine(datetime.today().date(), exit_.time)

                time_difference = time_exit - time_entry
                total_work_duration += time_difference

                total_duration = timedelta(seconds=total_work_duration.total_seconds())

                total_seconds = total_duration.total_seconds()

                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                duration_formatted = f"{hours:.0f}h {minutes:.0f}min {seconds:.0f}s"

            report.append({
                'Employe_nom': employe.nom,
                'Employe_prenom': employe.prenom,
                'premier_entre': first_entry.time if first_entry else 'No entry recorded',
                'dernier_sortie': last_exit.time if last_exit else 'No exit recorded',
                'total_work_duration': f'{duration_formatted}'
            })

        # Prepare the email content
        subject = f'Daily Employee Entry/Exit Report - {current_date}'
        message = '\n'.join(report)
        from_email = 'be.labzour@gmail.com'
        to_email = ['be.labzour@gmail.com']

        # Send the email
        send_mail(subject, message, from_email, to_email)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.remove_all_jobs()
    scheduler.add_job(schedule_email, 'interval', days=1, start_date='2023-06-09 20:00:00')
    if os.environ.get('RUN_MAIN'):
        scheduler.start()
