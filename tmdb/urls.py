from django.urls import path

from . import views

view = views.WatchList.as_view()

urlpatterns = [
    path('', view, name='add'),
    path('<int:wlid>', view, name='edit'),
    path('list', views.UserWatchList.as_view())
]
