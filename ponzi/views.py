from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.http import HttpResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import RegisterForm
from .models import AddressPair
from .utils import get_server
# Create your views here.

class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return '/add/'

index = IndexView.as_view()

class AddView(FormView):
    template_name = 'ponzi/add.html'
    form_class = RegisterForm
    success_url = '/list/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        instance = form.save()

        server = get_server()
        user_addr = instance.user_addr
        site_addr = server.getaccountaddress(user_addr)
        instance.site_addr = site_addr
        instance.save()

        return super(AddView, self).form_valid(form)

add = AddView.as_view()

def addr_list(request):
    addresspair_list = AddressPair.objects.all()
    paginator = Paginator(addresspair_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        addresspairs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        addresspairs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        addresspairs = paginator.page(paginator.num_pages)

    return render(request, 'ponzi/addr_list.html', {'addresspairs': addresspairs})

def callback(request):
    from ponzi.utils import process_tx
    if request.GET['transaction_hash']:
        process_tx(request.GET['transaction_hash'])
