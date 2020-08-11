from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from core.models import Job, Category



class HomeView(ListView):
    template_name = 'index.html'
    # context_object_name = "jobs"
    model = Job
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['jobs'] = Job.objects.all()
        context['categories'] = Category.objects.all()
        return context