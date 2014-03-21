# -*- coding: utf-8 -*-
 
from django.forms import ModelForm
from models import Order
from django.conf import settings
from livesettings import config_value
from django.core.mail import send_mail
from django.template import Context, Template


def sendmail(subject, body):
    mail_subject = ''.join(subject)
    send_mail(mail_subject, body, settings.DEFAULT_FROM_EMAIL,
        [config_value('MyApp', 'EMAIL')])

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('date', )
      
    def save(self, *args, **kwargs):
        super(OrderForm, self).save(*args, **kwargs)
        if 'card' in self.data:
            subject=u'Новая запись на тренировку'
        else:
            subject=u'Поступила новая заявка'
        
        body_templ="""
{% for field in form %}
   {{ field.label }} - {{ field.value }}
{% endfor %}

* Если заполнен комментарий - то это заявка на подарочный сертификат
* Если заполнена дата-время тренировки - то заявка на тренировку
* Если оба поля не заполнены, то лучше уточнить, на что заявка
            """
        ctx = Context({
            'form': self,

        })
        body = Template(body_templ).render(ctx)
        sendmail(subject, body)
