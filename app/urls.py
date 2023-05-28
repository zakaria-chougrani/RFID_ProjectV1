from django.urls import path, re_path
from . import views, exporter
from .views import connect_to_mqtt
from django.urls import path, include

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("list_employes", views.list_employes, name="list_employes"),
    path("details/<int:pk>", views.details_employe, name="details"),
    path("add_employe", views.add_employe, name="add_employe"),
    path("update_employe/<int:pk>", views.update_employe, name="update_employe"),
    path('employe/<int:pk>/delete/', views.delete_employe_view, name='delete_employe'),
    path('csv/<int:pk>', exporter.export_csv, name='export_csv'),
    path('compte/', include('compte.urls')),
]
connect_to_mqtt()
