import os
import importlib
from populate_YouHate import populate
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class IndexPageTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('YouHate.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('videoapp_project.urls')

    def test_view_exists(self):
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The index() view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The index() view is not callable.{FAILURE_FOOTER}")

    def test_mappings_exists(self):
        index_mapping_exists = False
        
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True
        
        self.assertTrue(index_mapping_exists, f"{FAILURE_HEADER}The index URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('index'), '/', f"{FAILURE_HEADER}The index URL lookup failed.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('index'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Requesting the index page failed.{FAILURE_FOOTER}")
        self.assertContains(response, "Welcome to the home page.", msg_prefix=f"{FAILURE_HEADER}The index view does not return the expected response.{FAILURE_FOOTER}")

class AboutPageTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('YouHate.views')
        self.views_module_listing = dir(self.views_module)
    
    def test_view_exists(self):
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The about() view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The about() view is not callable.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        self.assertEquals(reverse('about'), '/about/', f"{FAILURE_HEADER}The about URL lookup failed.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the about view, the server did not respond correctly.{FAILURE_FOOTER}")
        self.assertContains(response, "YouHate is a website", msg_prefix=f"{FAILURE_HEADER}The about view did not respond with the expected message.{FAILURE_FOOTER}")

class CategoryPageTests(TestCase):
    pass

class VideoPageTests(TestCase):
    pass

class ProfilePageTests(TestCase):
    pass

class RegisterPageTests(TestCase):
    pass

class LoginPageTests(TestCase):
    pass

class TemplateTests(TestCase):

    def get_template(self, path_to_template):
        f = open(path_to_template, 'r')
        template_str = ""

        for line in f:
            template_str = f"{template_str}{line}"

        f.close()
        return template_str
    
    def test_base_template_exists(self):
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'YouHate', 'base.html')
        self.assertTrue(os.path.exists(template_base_path), f"{FAILURE_HEADER}Failed to find the base.html template.{FAILURE_FOOTER}")
    
    def test_template_usage(self):
        
        populate()
        
        urls = [reverse('about'),
                #reverse('login'),
                reverse('register'),
                reverse('user_profile', kwargs={'username': 'user1'}),
                reverse('random_video'),
                reverse('category_detail', kwargs={'category_slug': 'music'}),
                #reverse('video_detail', kwargs={'category_slug': 'music', 'video_slug': ''}),
                reverse('index'),
                ]

        templates = ['YouHate/about.html',
                     #'YouHate/login.html',
                     'YouHate/register.html',
                     'YouHate/profile.html',
                     'YouHate/video_detail.html',
                     'YouHate/category_detail.html',
                     #'YouHate/video_detail.html',
                     'rango/index.html',]
        
        for url, template in zip(urls, templates):
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)

    def test_title_blocks(self):
        """
        Tests whether the title blocks in each page are the expected values.
        This is probably the easiest way to check for blocks.
        """
        populate()
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'rango')
        
        mappings = {
            reverse('rango:about'): {'full_title_pattern': r'<title>(\s*|\n*)Rango(\s*|\n*)-(\s*|\n*)About Rango(\s*|\n*)</title>',
                                     'block_title_pattern': r'{% block title_block %}(\s*|\n*)About Rango(\s*|\n*){% (endblock|endblock title_block) %}',
                                     'template_filename': 'about.html'},
            reverse('rango:add_category'): {'full_title_pattern': r'<title>(\s*|\n*)Rango(\s*|\n*)-(\s*|\n*)Add a Category(\s*|\n*)</title>',
                                            'block_title_pattern': r'{% block title_block %}(\s*|\n*)Add a Category(\s*|\n*){% (endblock|endblock title_block) %}',
                                            'template_filename': 'add_category.html'},
            reverse('rango:add_page', kwargs={'category_name_slug': 'python'}): {'full_title_pattern': r'<title>(\s*|\n*)Rango(\s*|\n*)-(\s*|\n*)Add a Page(\s*|\n*)</title>',
                                                                                 'block_title_pattern': r'{% block title_block %}(\s*|\n*)Add a Page(\s*|\n*){% (endblock|endblock title_block) %}',
                                                                                 'template_filename': 'add_page.html'},
            reverse('rango:show_category', kwargs={'category_name_slug': 'python'}): {'full_title_pattern': r'<title>(\s*|\n*)Rango(\s*|\n*)-(\s*|\n*)Python(\s*|\n*)</title>',
                                                                                      'block_title_pattern': r'{% block title_block %}(\s*|\n*){% if category %}(\s*|\n*){{ category.name }}(\s*|\n*){% else %}(\s*|\n*)Unknown Category(\s*|\n*){% endif %}(\s*|\n*){% (endblock|endblock title_block) %}',
                                                                                      'template_filename': 'category.html'},
            reverse('rango:index'): {'full_title_pattern': r'<title>(\s*|\n*)Rango(\s*|\n*)-(\s*|\n*)Homepage(\s*|\n*)</title>',
                                     'block_title_pattern': r'{% block title_block %}(\s*|\n*)Homepage(\s*|\n*){% (endblock|endblock title_block) %}',
                                     'template_filename': 'index.html'},
        }

        for url in mappings.keys():
            full_title_pattern = mappings[url]['full_title_pattern']
            template_filename = mappings[url]['template_filename']
            block_title_pattern = mappings[url]['block_title_pattern']

            request = self.client.get(url)
            content = request.content.decode('utf-8')
            template_str = self.get_template(os.path.join(template_base_path, template_filename))

            self.assertTrue(re.search(full_title_pattern, content), f"{FAILURE_HEADER}When looking at the response of GET '{url}', we couldn't find the correct <title> block. Check the exercises on Chapter 8 for the expected title.{FAILURE_FOOTER}")
            self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}When looking at the source of template '{template_filename}', we couldn't find the correct template block. Are you using template inheritence correctly, and did you spell the title as in the book? Check the exercises on Chapter 8 for the expected title.{FAILURE_FOOTER}")
    
    def test_for_links_in_base(self):
        """
        There should be three hyperlinks in base.html, as per the specification of the book.
        Check for their presence, along with correct use of URL lookups.
        """
        template_str = self.get_template(os.path.join(settings.TEMPLATE_DIR, 'rango', 'base.html'))

        look_for = [
            '<a href="{% url \'rango:add_category\' %}">Add a New Category</a>',
            '<a href="{% url \'rango:about\' %}">About</a>',
            '<a href="{% url \'rango:index\' %}">Index</a>',
        ]
        
        for lookup in look_for:
            self.assertTrue(lookup in template_str, f"{FAILURE_HEADER}In base.html, we couldn't find the hyperlink '{lookup}'. Check your markup in base.html is correct and as written in the book.{FAILURE_FOOTER}")