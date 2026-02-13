from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_memories, name='index'),
    path('list/', views.get_memories, name='get_memories'),
    path('list/tag/<str:tag>/', views.get_memories, name='get_memories_tagged'),
    path('list/type/<str:type>/', views.get_memories, name='get_memories_types'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('new/', views.save_memo, name='new_entry'),
    path('archive/<int:id>', views.archive_memo, name='move_entry_to_archive'),
    path('update/<int:id>', views.update_memo, name='update_entry'),
    path('delete/<int:id>', views.delete_memo, name='delete_entry'),
]
