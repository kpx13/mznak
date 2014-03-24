# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
 

from order.forms import OrderForm
from order.models import Order
from review.models import Review
from slideshow.models import Slider
from textblock.models import TextBlock

import config
from django.conf import settings
from livesettings import config_value
import datetime

PAGINATION_COUNT = 5

def get_common_context(request):
    form = OrderForm()
    c = {}
    if request.method == 'POST':
        if request.POST['action'] == 'order':
            form = OrderForm(request.POST)
            if form.is_valid():
                form.save()
                c['request-ok'] = True
            else:
                messages.error(request, u'Необходимо ввести имя.')

    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['form'] = form
    c['phone'] = config_value('MyApp', 'PHONE')
    ORDERS_COUNT = int(config_value('MyApp', 'ORDERS_COUNT'))
    c['oc_3'] = ORDERS_COUNT % 10
    ORDERS_COUNT = ORDERS_COUNT / 10
    c['oc_2'] = ORDERS_COUNT % 10
    c['oc_1'] = ORDERS_COUNT / 10
    c.update(csrf(request))
    return c

def home(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['slider'] = Slider.objects.all()
    c['reviews'] = Review.objects.all()
    c['textblocks'] = TextBlock.objects.all()
    return render_to_response('index.html', c, context_instance=RequestContext(request))