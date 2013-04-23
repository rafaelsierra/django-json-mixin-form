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
        import ipdb;ipdb.set_trace()