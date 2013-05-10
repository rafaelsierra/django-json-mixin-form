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
        - include_hidden_fields = True # Whether to include invalid hidden fields in the response
        - hidden_field_error_key = 'hidden_fields_errors' # Key to use for invalid hidden fields
        
        
    Returns:
    {
        'success': bool, // Set only when View.include_success = True (default)
        'non_field_errors': [error_list], // Same as form.non_field_errors,
        'hidden_fields_errors': { /* same as 'errors' */} // May be empty
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
    include_hidden_fields = True
    hidden_field_error_key = 'hidden_fields_errors'
    
    def _render_json(self, response_object):
        # http://www.ietf.org/rfc/rfc4627.txt
        return HttpResponse(json.dumps(response_object, encoding=self.json_encoding), content_type='application/json')

    
    def _get_field_error_dict(self, field):
        '''Returns the dict containing the field errors information'''
        return {
            'name': field.html_name,
            'id': 'id_{}'.format(field.html_name), # This may be a problem
            'errors': field.errors,
        }
    
    
    def get_hidden_fields_errors(self, form):
        '''Returns a dict to add in response when something is wrong with hidden fields'''
        if not self.include_hidden_fields or form.is_valid():
            return {}
        
        response = {self.hidden_field_error_key:{}}
        
        for field in form.hidden_fields():
            if field.errors:
                response[self.hidden_field_error_key][field.html_name] = self._get_field_error_dict(field)            
        return response
    
        
    def form_valid(self, form):
        response = {self.errors_key: {}}
        response.update(self.get_hidden_fields_errors(form))
            
        if self.include_success:
            response[self.sucess_key] = True
            
        return self._render_json(response)
    
    
    def form_invalid(self, form):
        '''Builds the JSON for the errors'''
        response = {self.errors_key: {}}
        response[self.non_field_errors_key] = form.non_field_errors()
        response.update(self.get_hidden_fields_errors(form))
        
        for field in form.visible_fields():
            if field.errors:
                response[self.errors_key][field.html_name] = self._get_field_error_dict(field)
                
        if self.include_success:
            response[self.sucess_key] = False
                        
        return self._render_json(response)
        