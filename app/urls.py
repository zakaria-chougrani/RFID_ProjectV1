from django.urls import path, re_path
from . import views
from .views import connect_to_mqtt

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("list_employes", views.list_employes, name="list_employes"),
    path("details/<int:pk>", views.details_employe, name="details"),
    path("add_employe", views.add_employe, name="add_employe"),
    path('employe/<int:pk>/delete/', views.delete_employe_view, name='delete_employe'),

]
connect_to_mqtt()
