================================
Django View Mixin for JSON Forms
================================

This is a Mixin for Classbased Form Views which renders the POST result in JSON
format.

=====
Usage
=====

Install the package (using virtualenv preferably) with `pip install sierra-django-json-mixin-form` 
or `easy_install sierra-django-json-mixin-form`

There is no need to configure anything in settings.py.

Import and use it (testmixins folder contains a simple usage)

::

    # myapp/views.py
    from sierra.dj.mixins.forms import JSONFormMixin
    
    from django.views.generic.edit import FormView
    from django import forms
    
    from myapp.models import MyModel
    
    # This can be any kind of form, from simple forms to ModelForms and beyond
    # You can also define custom validation either on Model or the form (or both)
    class MyModelForm(forms.ModelForm): 
        class Meta:
            model = MyModel
        
    
    # Extends JSONFormMixin before your FormView or any extension of it which
    # does not returns an HttpResponse instance on form_valid and form_invalid
    # methods 
    class MyFormView(JSONFormMixin, FormView):
        form_class = FormTest
        template_name = 'my-form.html'
        # success_url = Unused
        

Add this view to your urls.py and call it via javascript.::

    # myproject/urls.py
    from django.conf.urls import patterns, include, url
    from myapp.views import MyFormView
    
    urlpatterns = patterns('',
        # ...
        url(r'^myform.json$', MyFormView.as_view(), name='my-form'),
    )


*NOTE:* This example is writing using jQuery, but you don't actually need any
Javascript library. I'm using jQuery just because it is easier.::

    # myscript.js
    $("#form").on('submit', function(){
        $.post("/myform.json", $(this).serialize(), function(response){
            if(response.success){
                // Horray!
            }else{
                // Do something with response.errors/non_field_errors
            }
        }, 'json');
        return false;
    });


Mixin options
=============

When writing your view you can set a bunch of attributes to change what it will
return in JSON:

* json_encoding = 'utf-8' # Encoding used to render JSON
* errors_key = 'errors' # Key used to group all errors
* non_field_errors_key = 'non_field_errors' # Key used for errors non related to fields
* include_success = False # In case of valid form, this will include a "success": true on JSON
* sucess_key = 'success' # Key used to signal success

To set any of these attributes, just set as class variable (or using self.<option>)::

    class MyView(JSONFormMixin, FormView):
        json_encoding = 'iso-8859-1'
        success_key = 'done'


Note that hidden fields are not supposed to not validate since they usually are 
set by the server, but anyway...
         

Response content
================

Depending on form validation JSON return will be something like this::

    {
        'success': bool, // Set only when View.include_success = True (default)
        'non_field_errors': [error_list], // Same as form.non_field_errors
        'errors': { // May be empty
            'field_name':{
                'name': 'field_name',
                'id': 'id_'+field_name, // Default Django HTML field ID
                'errors': [field_error_list] // Same as form.field.errors
            }
        }
    }
