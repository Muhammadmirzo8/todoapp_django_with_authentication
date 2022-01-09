from django.views.generic.base import View
from django.shortcuts import redirect
from django.views.generic.list import ListView  
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.urls import reverse_lazy 

from django.contrib.auth.views import LoginView 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

from .models import Task   

from django.forms.widgets import SelectDateWidget


class ULoginView(LoginView): 
    template_name = 'todo/login.html' 
    fields = '__all__' 
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks-list') 

class RegisterUserView(FormView):
    template_name = 'todo/register.html'  
    form_class = UserCreationForm
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks-list')
    
    def form_valid(self, form): 
        user = form.save() 
        if user is not None: 
            login(self.request, user)
        return super(RegisterUserView, self).form_valid(form)
        
    def get(self, request, *args, **kwargs): 
        if self.request.user.is_authenticated: 
            return redirect('tasks-list')
        return super(RegisterUserView, self).get( *args, **kwargs)

class TasksListView(LoginRequiredMixin, ListView): 
    model = Task
    context_object_name = 'tasks'    

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['tasks'] = context['tasks'].filter(user=self.request.user)  
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

class TaskDetailView(LoginRequiredMixin, DetailView): 
    model = Task 
    context_object_name = 'task'  
    template_name = 'todo/task.html' 

class TaskCreateView(LoginRequiredMixin, CreateView): 
    model = Task   
    fields = ['title', 'description', 'deadline', 'complete', ]
    success_url = reverse_lazy('tasks-list')  
    
    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)
        
    def get_form(self):
        '''add date picker in forms'''
        form = super(TaskCreateView, self).get_form()
        form.fields['deadline'].widget = SelectDateWidget()

        return form
class TaskUpdateView(LoginRequiredMixin, UpdateView): 
    model = Task   
    fields = ['title', 'description', 'deadline', 'complete', ]
    success_url = reverse_lazy('tasks-list')   
    

class DeleteView(LoginRequiredMixin, View): 
    def get(self, request, pk,):  
        Task.objects.get(id=pk, user=self.request.user).delete()
        return redirect('/') 


