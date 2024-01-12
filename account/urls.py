from django.urls import path, reverse
from . import views
from django.views.generic import RedirectView

app_name = 'account'

urlpatterns = [
    # path('', RedirectView.as_view(url=(reverse('progress:home'))))
]
