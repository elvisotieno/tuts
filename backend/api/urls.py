from django.urls import path
from .views import diseases_list, detail


urlpatterns = [
    path('diseases/', diseases_list),
    path('detail/<int:pk>/', detail)
]