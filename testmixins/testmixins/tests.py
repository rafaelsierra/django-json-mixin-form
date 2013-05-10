# -*- coding: utf-8 -*-
import json
from django.utils import unittest
from django.test.client import Client


class FormJSONMixinTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

        
    def make_request(self, url, postdata):
        '''Makes the request and parses the json response'''
        return json.loads(self.client.post(url, postdata).content)

        
    def test_valid_fields(self):
        response = self.make_request('/', {'name':'Valid name', 'email': 'valid@email.asd'})
        self.assertDictEqual(response['errors'], {})
        
    
    def test_invalid_name(self):
        # 'name' is required
        response = self.make_request('/', {'email': 'valid@email.asd'})
        self.assertIn('name', response['errors'])
        self.assertNotIn('email', response['errors'])
        
    
    def test_invalid_email(self):
        response = self.make_request('/', {'email': 'valid#email.asd', 'name':'Valid name'})
        self.assertIn('email', response['errors'])
        self.assertNotIn('name', response['errors'])        
        
    def test_hidden_field_error(self):
        '''Tests the behavior of hidden fields'''
        response = self.make_request('/hidden-fields/', {'token': '1234'})
        self.assertNotIn('hidden_fields_errors', response)
        
        response = self.make_request('/hidden-fields/', {})
        self.assertIn('hidden_fields_errors', response)
        self.assertIn('token', response['hidden_fields_errors'])
        