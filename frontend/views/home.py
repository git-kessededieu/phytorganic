from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, ListView, DetailView

from backend.forms import MemberForm
from frontend.forms import MigrationForm
from frontend.models import Product, FAQ


class FrontMenuView(TemplateView):
    template_name = 'frontend/partials/header.html'

    def get(self, request, *args, **kwargs):
        form = MigrationForm()
        context = {
            'page_name': self.kwargs['page_name'],
            'products': Product.objects.all(),
            'form': form
        }

        return TemplateResponse(request, self.template_name, context)


class MigrationView(TemplateView):

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            member.save()

            messages.success(request, "You've successfully completed the migration form, see you soon!")
            return redirect('frontend:home')


class WelcomeView(TemplateView):
    def get(self, request, new_context = None, *args, **kwargs):
        if new_context is None:
            new_context = {}
        form = MigrationForm()
        context = {
            'page_name': 'landing',
            'page_title': _('Welcome to phytorganic.net'),
            'form': form
        }
        context.update(new_context)
        return render(request, 'frontend/landing.html', context)

    def post(self, request, *args, **kwargs):
        form = MigrationForm(request.POST)
        if form.is_valid():
            migration = form.save()
            migration.save()

            context = {
                'status': 'success'
            }
            response = self.get(request, context)
            return response


class HomeView(TemplateView):
    template_name = 'frontend/common/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = "home"
        context['page_title'] = _("Home")
        print("KWARGS => {}".format(self.kwargs))
        username = self.kwargs.get("username", None)
        # del self.request.session["username"]
        if username is not None:
            self.request.session['username'] = username

        print("Username => {}".format(self.request.session.get('username')))
        return context


class AboutView(TemplateView):
    template_name = 'frontend/common/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = "about"
        context['page_title'] = _("About")
        return context


class ProductListView(ListView):
    template_name = 'frontend/common/products.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = "products"
        context['page_title'] = _("Products")
        return context


class ProductDetailsView(DetailView):
    template_name = 'frontend/common/product.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = "product"
        context['page_title'] = _(self.object.name)
        return context


class FAQView(ListView):
    template_name = 'frontend/common/faq.html'
    model = FAQ

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_name'] = "faq"
        context['page_title'] = _("F.A.Q.")
        return context
