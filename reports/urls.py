from django.urls import path

from . import views

urlpatterns = [
    path('<int:report_id>', views.Reports.as_view(), name='reports'),
]
