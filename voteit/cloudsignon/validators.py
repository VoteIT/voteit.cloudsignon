import colander

from pyramid.traversal import find_root

from voteit.cloudsignon import VoteITCSO as _


class UniqueOauthAccessToken(object):
    """ Check that oauth access token unique.
    """
    def __init__(self, context):
        self.context = context

    def __call__(self, node, value):
        root = find_root(context)
        users = root.users
        match = users.get_user_by_oauth_token(value)
        if match:
            msg = _(u"oauth_access_token_not_unique_error",
                    default=u"Another user has already registered with this token.")
            raise colander.Invalid(node, 
                                   msg)
        
def deferred_unique_oauth_access_token_validator(node, kw):
    """ When called from cloud_login_complete view kw is not a dict
    """
    if 'context' in kw:
        context = kw['context']
    else:
        context = None    
    return UniqueOauthAccessToken(context)