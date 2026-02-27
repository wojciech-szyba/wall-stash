"""
 Copyright (C) 2026 Wojciech Szyba - All Rights Reserved
 You may use, distribute and modify this code under the
 terms of the GNU GENERAL PUBLIC LICENSE license,
 You should have received a copy of the license with
 this file. If not, please visit :
https://github.com/wojciech-szyba/stash-wall/blob/main/LICENSE
 */
"""

from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_memories, name='index'),
    path('list/', views.get_memories, name='get_memories'),
    path('list/tag/<str:tag>/', views.get_memories, name='get_memories_tagged'),
    path('list/type/<str:type>/', views.get_memories, name='get_memories_types'),
    path('list/date/<str:date>/', views.get_memories, name='get_memories_date'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('new/', views.save_memo, name='new_entry'),
    path('archive/<int:id>', views.archive_memo, name='move_entry_to_archive'),
    path('update/<int:id>', views.update_memo, name='update_entry'),
    path('delete/<int:id>', views.delete_memo, name='delete_entry'),
]
