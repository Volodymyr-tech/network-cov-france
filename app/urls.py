from django.urls import path
from .views import MobileSiteByCityView

urlpatterns = [
    path('coverage/', MobileSiteByCityView.as_view(), name='mobile-site-by-city'),
]
