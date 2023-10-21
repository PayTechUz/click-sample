from django.urls import path

from shop.views import MyView

urlpatterns = [
    path('click/merchant/', MyView.as_view())
]
