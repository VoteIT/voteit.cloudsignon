import unittest

from pyramid import testing
from zope.interface.verify import verifyObject

    
class FacebookProfileImageUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
    
    def _make_obj(self):
        from voteit.cloudsignon.profile_image_plugins import FacebookProfileImagePlugin
        from voteit.core.models.user import User
        from voteit.core.models.site import SiteRoot 

        root = SiteRoot()
        root['user'] = User()
        root['user'].auth_domains['facebook'] = {'oauth_userid': 'oauth_userid'}
        
        return FacebookProfileImagePlugin( root['user'] )

    def test_verify_implementation(self):
        from voteit.core.models.interfaces import IProfileImage
        obj = self._make_obj()
        self.assertTrue(verifyObject(IProfileImage, obj))
        
    def test_url_method(self):
        obj = self._make_obj()
        url = obj.url(size=45)
        self.assertEqual(url,
                         'http://graph.facebook.com/oauth_userid/picture')

    def test_is_valid(self):
        obj = self._make_obj()
        self.assertTrue(obj.is_valid_for_user())


class TwitterProfileImageUnitTests(unittest.TestCase):
    
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
    
    def _make_obj(self):
        from voteit.cloudsignon.profile_image_plugins import TwitterProfileImagePlugin
        from voteit.core.models.user import User
        from voteit.core.models.site import SiteRoot 

        root = SiteRoot()
        root['user'] = User()
        root['user'].auth_domains['twitter'] = {'oauth_userid': 'oauth_userid', 'display_name': 'display_name'}
        
        return TwitterProfileImagePlugin( root['user'] )

    def test_verify_implementation(self):
        from voteit.core.models.interfaces import IProfileImage
        obj = self._make_obj()
        self.assertTrue(verifyObject(IProfileImage, obj))
        
    def test_url_method(self):
        obj = self._make_obj()
        url = obj.url(size=45)
        self.assertEqual(url,
                         'http://api.twitter.com/1/users/profile_image?screen_name=display_name&size=bigger')

    def test_is_valid(self):
        obj = self._make_obj()
        self.assertTrue(obj.is_valid_for_user())
