from django.test import TestCase
from django.shortcuts import redirect
# Create your tests here.

class IndexTest(TestCase):


    def test_get(self):
        response = self.client.get(redirect('create_agent'))
        self.assertTemplateUsed(response,'create_agent.html')
    

