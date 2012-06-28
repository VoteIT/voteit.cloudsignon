import unittest

from pyramid import testing
from pyramid.exceptions import Forbidden
from pyramid_mailer import get_mailer
from webob.multidict import MultiDict

from voteit.core.testing_helpers import bootstrap_and_fixture


class UsersViewTests(unittest.TestCase):
        
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
    
    @property
    def _cut(self):
        from voteit.cloudsignon.views import CloudSignOnView
        return CloudSignOnView
    
    def _fixture(self):
        from voteit.core.models.user import User
        root = bootstrap_and_fixture(self.config)
        root.users['dummy1'] = User(title='Dummy 1')
        root.users['dummy1'].auth_domains['facebook'] = {'oauth_access_token': 'dummy1_token', 
                                                         'oauth_userid': 'dummy1_userid'}
        root.users['dummy1'].auth_domains['twitter'] = {'oauth_access_token': 'dummy1_token', 
                                                         'oauth_userid': 'dummy1_userid'}
        root.users['dummy2'] = User(title='Dummy 2')
        root.users['dummy3'] = User(title='Dummy 3')
        return root
    
    def test_facebook_register(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(permissive=False)
        context = self._fixture()
        request = testing.DummyRequest()
        obj = self._cut(context, request)
        self.assertRaises(Forbidden, obj.facebook_register)
        
    def test_facebook_register_cancel(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post={'cancel': 'cancel'})
        obj = self._cut(context, request)
        response = obj.facebook_register()
        self.assertEqual(response.location, 'http://example.com/')
        
    def test_facebook_register_post(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post = MultiDict([('userid', 'dummy4'),
                                                         ('oauth_access_token', 'dummy_token'), 
                                                         ('oauth_userid', 'dummy_userid'),
                                                         ('email', 'dummy@test.com'), 
                                                         ('first_name', 'Dummy'), 
                                                         ('last_name', 'Person'), 
                                                         ('came_from', '/'), 
                                                         ('register', 'register')]))
        obj = self._cut(context, request)
        response = obj.facebook_register()
        self.assertIn('dummy4', context.users)
        self.assertEqual(response.location, 'http://example.com/')
        self.assertIn('facebook', context.users['dummy4'].auth_domains)
        self.assertEqual(context.users['dummy4'].auth_domains['facebook']['oauth_access_token'], 'dummy_token')
        
    def test_facebook_register_token_already_used(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(userid='dummy3', permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post = MultiDict([('userid', 'dummy3'),
                                                         ('oauth_access_token', 'dummy1_token'), 
                                                         ('oauth_userid', 'dummy1_userid'),
                                                         ('email', 'dummy@test.com'), 
                                                         ('first_name', 'Dummy'), 
                                                         ('last_name', 'Person'), 
                                                         ('came_from', '/'), 
                                                         ('register', 'register')]))
        obj = self._cut(context, request)
        self.assertRaises(Forbidden, obj.facebook_register)
        
    def test_facebook_register_connect(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(userid='dummy3', permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post = MultiDict([('userid', 'dummy3'),
                                                         ('oauth_access_token', 'dummy3_token'), 
                                                         ('oauth_userid', 'dummy3_userid'),
                                                         ('email', 'dummy@test.com'), 
                                                         ('first_name', 'Dummy'), 
                                                         ('last_name', 'Person'), 
                                                         ('came_from', '/'), 
                                                         ('register', 'register')]))
        obj = self._cut(context, request)
        response = obj.facebook_register()
        self.assertEqual(response.location, 'http://example.com/users/dummy3/')
        self.assertIn('facebook', context.users['dummy3'].auth_domains)
        self.assertEqual(context.users['dummy3'].auth_domains['facebook']['oauth_access_token'], 'dummy3_token')
        
    def test_facebook_register_login(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post = MultiDict([('userid', 'dummy4'),
                                                         ('oauth_access_token', 'dummy1_token'), 
                                                         ('oauth_userid', 'dummy1_userid'),
                                                         ('email', 'dummy@test.com'), 
                                                         ('first_name', 'Dummy'), 
                                                         ('last_name', 'Person'), 
                                                         ('came_from', '/'), 
                                                         ('register', 'register')]))
        obj = self._cut(context, request)
        response = obj.facebook_register()
        self.assertEqual(response.location, 'http://example.com/')
        
        
    def test_twitter_register(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(permissive=False)
        context = self._fixture()
        request = testing.DummyRequest()
        obj = self._cut(context, request)
        self.assertRaises(Forbidden, obj.twitter_register)
        
    def test_twitter_register_cancel(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post={'cancel': 'cancel'})
        obj = self._cut(context, request)
        response = obj.twitter_register()
        self.assertEqual(response.location, 'http://example.com/')
        
    def test_twitter_register_post(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post = MultiDict([('userid', 'dummy4'),
                                                         ('oauth_access_token', 'dummy_token'), 
                                                         ('oauth_userid', 'dummy_userid'),
                                                         ('email', 'dummy@test.com'), 
                                                         ('first_name', 'Dummy'), 
                                                         ('last_name', 'Person'), 
                                                         ('came_from', '/'), 
                                                         ('register', 'register')]))
        obj = self._cut(context, request)
        response = obj.twitter_register()
        self.assertIn('dummy4', context.users)
        self.assertEqual(response.location, 'http://example.com/')
        self.assertIn('twitter', context.users['dummy4'].auth_domains)
        self.assertEqual(context.users['dummy4'].auth_domains['twitter']['oauth_access_token'], 'dummy_token')
        
    def test_twitter_register_token_already_used(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(userid='dummy3', permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post = MultiDict([('userid', 'dummy3'),
                                                         ('oauth_access_token', 'dummy1_token'), 
                                                         ('oauth_userid', 'dummy1_userid'),
                                                         ('email', 'dummy@test.com'), 
                                                         ('first_name', 'Dummy'), 
                                                         ('last_name', 'Person'), 
                                                         ('came_from', '/'), 
                                                         ('register', 'register')]))
        obj = self._cut(context, request)
        self.assertRaises(Forbidden, obj.twitter_register)
        
    def test_twitter_register_connect(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(userid='dummy3', permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post = MultiDict([('userid', 'dummy3'),
                                                         ('oauth_access_token', 'dummy3_token'), 
                                                         ('oauth_userid', 'dummy3_userid'),
                                                         ('email', 'dummy@test.com'), 
                                                         ('first_name', 'Dummy'), 
                                                         ('last_name', 'Person'), 
                                                         ('came_from', '/'), 
                                                         ('register', 'register')]))
        obj = self._cut(context, request)
        response = obj.twitter_register()
        self.assertEqual(response.location, 'http://example.com/users/dummy3/')
        self.assertIn('twitter', context.users['dummy3'].auth_domains)
        self.assertEqual(context.users['dummy3'].auth_domains['twitter']['oauth_access_token'], 'dummy3_token')
        
    def test_twitter_register_login(self):
        self.config.scan('voteit.cloudsignon.schemas')
        self.config.include('voteit.core.models.flash_messages')
        self.config.testing_securitypolicy(permissive=False)
        context = self._fixture()
        request = testing.DummyRequest(post = MultiDict([('userid', 'dummy4'),
                                                         ('oauth_access_token', 'dummy1_token'), 
                                                         ('oauth_userid', 'dummy1_userid'),
                                                         ('email', 'dummy@test.com'), 
                                                         ('first_name', 'Dummy'), 
                                                         ('last_name', 'Person'), 
                                                         ('came_from', '/'), 
                                                         ('register', 'register')]))
        obj = self._cut(context, request)
        response = obj.twitter_register()
        self.assertEqual(response.location, 'http://example.com/')