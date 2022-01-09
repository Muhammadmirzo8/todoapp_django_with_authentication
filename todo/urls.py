from django.urls import path
from todo.views import TasksListView, TaskDetailView, TaskCreateView, TaskUpdateView, DeleteView, ULoginView, RegisterUserView
from django.contrib.auth.views import LogoutView


urlpatterns = [ 
    path('login/',ULoginView.as_view(), name="login" ),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),

    path('', TasksListView.as_view(), name="tasks-list"), 
    path('task/<int:pk>/', TaskDetailView.as_view(), name="task-detail"), 
    path('task-create', TaskCreateView.as_view(), name="task-create"), 
    path('task/update/<int:pk>/', TaskUpdateView.as_view(), name="task-update"),  
    path('task/delete/<int:pk>/', DeleteView.as_view(), name="task-delete"),
] 
