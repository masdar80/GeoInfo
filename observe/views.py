from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
# from .mixins import SuccessUrlMixin


class BaseListView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model': self.model
        })
        return context


class BaseCreateView(CreateView):
    pass


class BaseUpdateView(UpdateView):
    pass


class BaseDeleteView(DeleteView):
    pass