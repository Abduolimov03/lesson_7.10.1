from django.urls import path
from .views import flower_list, flower_create, flower_delete, flower_detail, flower_update

urlpatterns = [
    path('flowers/', flower_list, name='flower_list'),
    path('flower/create/', flower_create, name='flower_create'),
    path('flower/<int:pk>/detail/', flower_detail, name='flower_detail'),
    path('flower/<int:pk>/delete/', flower_delete, name='flower_delete'),
    path('flower/<int:pk>/update/', flower_update, name='flower_update'),

]