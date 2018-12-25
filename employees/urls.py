from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.profile, name='empl-profile'),
    path('<int:pk>/update', views.update, name='empl-update'),
    path('<int:pk>/delete', views.delete, name='empl-delete'),
    path('create/', views.create, name='empl-create'),
    path('seed/', views.seed, name='empl-seed'),
    path('list/', views.list, name='empl-list'),
    path('list/search', views.search),
    path('tree/', views.tree, name='empl-tree'),
    path('tree/open', views.tree_lazy_open),
    path('tree/replace', views.change_super),
]