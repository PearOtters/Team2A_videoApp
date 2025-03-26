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
        self.project_urls_module = importlib.import_module('videoapp_project.urls')
    
    def test_view_exists(self):
        name_exists = 'about' in self.views_module_listing
        is_callable = callable(self.views_module.about)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The about() view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The about() view is not callable.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        about_mapping_exists = False
        
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'about':
                    about_mapping_exists = True
        
        self.assertTrue(about_mapping_exists, f"{FAILURE_HEADER}The about URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('about'), '/about/', f"{FAILURE_HEADER}The about URL lookup failed.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('about'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the about view, the server did not respond correctly.{FAILURE_FOOTER}")
        self.assertContains(response, "YouHate is a website", msg_prefix=f"{FAILURE_HEADER}The about view did not respond with the expected message.{FAILURE_FOOTER}")

class CategoryPageTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('YouHate.views')
        self.views_module_listing = dir(self.views_module)
        self.project_urls_module = importlib.import_module('videoapp_project.urls')

        populate()
    
    def test_view_exists(self):
        name_exists = 'category_detail' in self.views_module_listing
        is_callable = callable(self.views_module.category_detail)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The category_detail() view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The category_detail() view is not callable.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        category_mapping_exists = False
        
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'category_detail':
                    category_mapping_exists = True
        
        self.assertTrue(category_mapping_exists, f"{FAILURE_HEADER}The category_detail URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('category_detail', kwargs={'category_slug': 'music'}), '/music/', f"{FAILURE_HEADER}The category_detail URL lookup failed.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('category_detail', kwargs={'category_slug': 'music'}))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the category_detail view, the server did not respond correctly.{FAILURE_FOOTER}")

class VideoPageTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('YouHate.views')
        self.views_module_listing = dir(self.views_module)
        self.project_urls_module = importlib.import_module('videoapp_project.urls')

        populate()
    
    def test_view_exists(self):
        name_exists = 'video_detail' in self.views_module_listing
        is_callable = callable(self.views_module.video_detail)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The video_detail() view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The video_detail() view is not callable.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        video_mapping_exists = False
        
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'video_detail':
                    video_mapping_exists = True
        
        self.assertTrue(video_mapping_exists, f"{FAILURE_HEADER}The video_detail URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('video_detail', kwargs={'category_slug': 'music', 'video_slug': 'KendrickLamarPop'}), '/music/KendrickLamarPop/', f"{FAILURE_HEADER}The video_detail URL lookup failed.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('video_detail', kwargs={'category_slug': 'music', 'video_slug': 'KendrickLamarPop'}))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the video_detail view, the server did not respond correctly.{FAILURE_FOOTER}")
        self.assertContains(response, "All The Stars Kendrick Lamar", msg_prefix=f"{FAILURE_HEADER}The video_detail view did not respond with the expected message.{FAILURE_FOOTER}")

class ProfilePageTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('YouHate.views')
        self.views_module_listing = dir(self.views_module)
        self.project_urls_module = importlib.import_module('videoapp_project.urls')

        populate()
    
    def test_view_exists(self):
        name_exists = 'user_profile' in self.views_module_listing
        is_callable = callable(self.views_module.user_profile)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The user_profile() view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The user_profile() view is not callable.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        profile_mapping_exists = False
        
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'user_profile':
                    profile_mapping_exists = True
        
        self.assertTrue(profile_mapping_exists, f"{FAILURE_HEADER}The user_profile URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('user_profile', kwargs={'username': 'user1'}), '/profile/user1/', f"{FAILURE_HEADER}The user_profile URL lookup failed.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('user_profile', kwargs={'username': 'user1'}))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the user_profile view, the server did not respond correctly.{FAILURE_FOOTER}")
        self.assertContains(response, "user1", msg_prefix=f"{FAILURE_HEADER}The user_profile view did not respond with the expected message.{FAILURE_FOOTER}")

class RegisterPageTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('YouHate.views')
        self.views_module_listing = dir(self.views_module)
        self.project_urls_module = importlib.import_module('videoapp_project.urls')

        populate()
    
    def test_view_exists(self):
        name_exists = 'user_register' in self.views_module_listing
        is_callable = callable(self.views_module.user_register)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The user_register() view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The user_register() view is not callable.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        register_mapping_exists = False
        
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'register':
                    register_mapping_exists = True
        
        self.assertTrue(register_mapping_exists, f"{FAILURE_HEADER}The register URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('register'), '/register/', f"{FAILURE_HEADER}The register URL lookup failed.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('register'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the user_register view, the server did not respond correctly.{FAILURE_FOOTER}")
        self.assertContains(response, "Register", msg_prefix=f"{FAILURE_HEADER}The user_register view did not respond with the expected message.{FAILURE_FOOTER}")

class LoginPageTests(TestCase):
    
    def setUp(self):
        self.views_module = importlib.import_module('YouHate.views')
        self.views_module_listing = dir(self.views_module)
        self.project_urls_module = importlib.import_module('videoapp_project.urls')

        populate()
    
    def test_view_exists(self):
        name_exists = 'sign_in_view' in self.views_module_listing
        is_callable = callable(self.views_module.sign_in_view)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The sign_in_view() view does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}The sign_in_view() view is not callable.{FAILURE_FOOTER}")
    
    def test_mapping_exists(self):
        login_mapping_exists = False
        
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'login':
                    login_mapping_exists = True
        
        self.assertTrue(login_mapping_exists, f"{FAILURE_HEADER}The login URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('login'), '/login/', f"{FAILURE_HEADER}The login URL lookup failed.{FAILURE_FOOTER}")
    
    def test_response(self):
        response = self.client.get(reverse('login'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}When requesting the login view, the server did not respond correctly.{FAILURE_FOOTER}")
        self.assertContains(response, "Sign In", msg_prefix=f"{FAILURE_HEADER}The login view did not respond with the expected message.{FAILURE_FOOTER}")


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
                reverse('login'),
                reverse('register'),
                reverse('user_profile', kwargs={'username': 'user1'}),
                reverse('category_detail', kwargs={'category_slug': 'music'}),
                reverse('video_detail', kwargs={'category_slug': 'music', 'video_slug': 'KendrickLamarPop'}),
                reverse('index'),
                ]

        templates = ['YouHate/about.html',
                     'YouHate/sign_in.html',
                     'YouHate/register.html',
                     'YouHate/profile.html',
                     'YouHate/category_detail.html',
                     'YouHate/video_detail.html',
                     'YouHate/index.html',]
        
        for url, template in zip(urls, templates):
            response = self.client.get(url)
            self.assertTemplateUsed(response, template)

    def test_for_links_in_base(self):
        template_str = self.get_template(os.path.join(settings.TEMPLATE_DIR, 'YouHate', 'base.html'))

        look_for = [
            '"{% url \'about\' %}"',
            '"{% url \'user_profile\' baseCurrentUser %}"',
            '"{% url \'login\' %}"',
            '"{% url \'index\' %}"',
            '"{% url \'random_video\' %}"',
            '"{% url \'category_detail\' slug %}"',
        ]
        
        for lookup in look_for:
            self.assertTrue(lookup in template_str, f"{FAILURE_HEADER}In base.html, failed to find '{lookup}'.{FAILURE_FOOTER}")