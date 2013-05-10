# -*- coding: utf-8 -*-
from sierra.dj.mixins.forms import JSONFormMixin
from django.views.generic.edit import FormView
from django import forms

class FormTest(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()



class FormWithHiddenField(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput)
    

class TestFormView(JSONFormMixin, FormView):
    form_class = FormTest
    template_name = 'empty.html'
    # success_url = Unused
    
    
class TestFormWithHiddenFieldView(JSONFormMixin, FormView):
    form_class = FormWithHiddenField
    template_name = 'empty.html'