from django.test import TestCase


class HomeTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/documents/')
        self.response_new = self.client.get('/documents/new/')

    def test_get(self):
        """Get /documents/ must return status code 200 """
        self.assertEqual(200, self.response.status_code)

    def test_get_new(self):
        """Get /documents/ must return status code 200 """
        self.assertEqual(200, self.response_new.status_code)

    def test_template(self):
        """ Must use documents/home.html """
        self.assertTemplateUsed(self.response, 'documents/home.html')

    def test_template_new(self):
        """ Must use documents/home.html """
        self.assertTemplateUsed(self.response_new, 'documents/new.html')

    def test_html_new(self):
        self.assertContains(self.response_new, '<form')
        self.assertContains(self.response_new, '<input', 4)
        self.assertContains(self.response_new, 'type="date"', 2)
        self.assertContains(self.response_new, 'type="textarea"', 0)
        self.assertContains(self.response_new, 'type="submit"')

    def test_csrf_html_new(self):
        """HTML must contains csrf"""
        self.assertContains(self.response_new, 'csrfmiddlewaretoken')