# -*- coding: utf-8 -*-
from django.http import HttpResponse

try:
    import json
except ImportError, e:
    from django.utils import simplejson as json
    
    

class JSONFormMixin(object):
    '''Returns a valid JSON response for using with Django Forms and "Ajax" 
    requests.
    
    Options:
        - json_encoding = 'utf-8' # Encoding used to render JSON
        - errors_key = 'errors' # Key used to group all errors
        - non_field_errors_key = 'non_field_errors' # Key used for errors non related to fields
        - include_success = False # In case of valid form, this will include a "success": true on JSON
        - sucess_key = 'success' # Key used to signal success
        
        
    Returns:
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
    '''
    
    json_encoding = 'utf-8'
    errors_key = 'errors'
    non_field_errors_key = 'non_field_errors'
    include_success = True
    sucess_key = 'success'

    
    def _render_json(self, response_object):
        # http://www.ietf.org/rfc/rfc4627.txt
        return HttpResponse(json.dumps(response_object, encoding=self.json_encoding), content_type='application/json')

    
    def form_valid(self, form):
        response = {self.errors_key: {}}
        if self.include_success:
            response[self.sucess_key] = True
            
        return self._render_json(response)
    
    
    def form_invalid(self, form):
        '''Builds the JSON for the errors'''
        response = {self.errors_key: {}}
        response[self.non_field_errors_key] = form.non_field_errors()
        
        for field in form.visible_fields():
            if field.errors:
                error = {
                    'name': field.html_name,
                    'id': 'id_{}'.format(field.html_name), # This may be a problem
                    'errors': field.errors,
                }
                response[self.errors_key][field.html_name] = error
                
        if self.include_success:
            response[self.sucess_key] = False
                        
        return self._render_json(response)
        