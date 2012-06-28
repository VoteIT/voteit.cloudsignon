from zope.interface import implements
from zope.component import adapts

from voteit.core.models.interfaces import IUser
from voteit.core.models.interfaces import IProfileImage

from voteit.cloudsignon import VoteITCSO as _


class FacebookProfileImagePlugin(object):
    implements(IProfileImage)
    adapts(IUser)
    
    name = u'facebook_profile_image'
    title = _('Facebook')
    description = _(u'facebook_profile_image_description', default=u'')
    
    def __init__(self, context):
        self.context = context
    
    def url(self, size):
        
        if not 'facebook' in self.context.auth_domains:
            return None

        oauth_userid = self.context.auth_domains['facebook']['oauth_userid']
        if not oauth_userid:
            return None
        
        url = 'http://graph.facebook.com/%(UID)s/picture?type=large' % {'UID': oauth_userid}
        
        return url
    
    def is_valid_for_user(self):
        if 'facebook' in self.context.auth_domains:
            oauth_userid = self.context.auth_domains['facebook']['oauth_userid']
            if oauth_userid:
                return True
        
        return False

    
class TwitterProfileImagePlugin(object):
    implements(IProfileImage)
    adapts(IUser)
    
    name = u'twitter_profile_image'
    title = _('Twitter')
    description = _(u'twitter_profile_image_description', default=u'')
    
    def __init__(self, context):
        self.context = context
    
    def url(self, size):
        
        if not 'twitter' in self.context.auth_domains:
            return None

        display_name = self.context.auth_domains['twitter']['display_name']
        if not display_name:
            return None
        
        url = 'http://api.twitter.com/1/users/profile_image?screen_name=%(screen_name)s&size=bigger' % {'screen_name': display_name}
        
        return url
    
    def is_valid_for_user(self):
        if 'twitter' in self.context.auth_domains:
            oauth_userid = self.context.auth_domains['twitter']['oauth_userid']
            if oauth_userid:
                return True
        
        return False


def includeme(config):
    """ Include gravatar plugin
    """
    config.registry.registerAdapter(FacebookProfileImagePlugin, (IUser,), IProfileImage, FacebookProfileImagePlugin.name)
    config.registry.registerAdapter(TwitterProfileImagePlugin, (IUser,), IProfileImage, TwitterProfileImagePlugin.name)
