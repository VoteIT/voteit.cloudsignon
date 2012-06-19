import colander
import json

from betahaus.pyracont.factories import createContent
from betahaus.pyracont.factories import createSchema
from deform import Form
from deform.exception import ValidationFailure
from pyramid.exceptions import Forbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.security import remember
from pyramid.traversal import find_root
from pyramid.url import resource_url
from pyramid.view import view_config
from velruse import AuthenticationComplete
from velruse import AuthenticationDenied
from velruse import login_url

from voteit.core.models.interfaces import ISiteRoot
from voteit.core.models.interfaces import IUser
from voteit.core.views.base_edit import BaseEdit
from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_register
from voteit.core.models.schemas import button_cancel
from voteit.core.validators import NEW_USERID_PATTERN

from voteit.cloudsignon import VoteITCSO as _


class CloudSignOnView(BaseEdit):        
    
    @view_config(context=ISiteRoot, name='cso', renderer="voteit.core.views:templates/base_edit.pt", permission=NO_PERMISSION_REQUIRED)
    def cso(self):
        
        schema = createSchema('CSORegisterUserSchema').bind(context=self.context, request=self.request)
        add_csrf_token(self.context, self.request, schema)
        form = Form(schema, buttons=(button_register,button_cancel,))
        self.api.register_form_resources(form)
        
        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(_(u"Canceled"))

            url = resource_url(self.context, self.request)
            return HTTPFound(location=url)

        if self.request.POST:
            post = dict(self.request.POST)
            if 'oauth_access_token' in post and post['oauth_access_token']:
                oauth_access_token = post['oauth_access_token']
                
                # Logged in user, connect auth token to user
                if self.api.userid:
                    current_user = self.api.user_profile
                    
                    #check that no other user has this token already
                    user = get_user_by_oauth_token(self.context, oauth_access_token)
                    if user and current_user != user:
                        raise Forbidden(_("Unable to Authenticate using OpenID"))
                    
                    current_user.set_field_value('oauth_access_token', oauth_access_token)
                    url = resource_url(current_user, self.request)
                    return HTTPFound(location=url)
                else:
                    # Find user with auth token and log it in
                    user = get_user_by_oauth_token(self.context, oauth_access_token)
                    if user:
                        if IUser.providedBy(user):
                            headers = remember(self.request, user.__name__)
                            url = resource_url(self.context, self.request)
                            return HTTPFound(location = url,
                                             headers = headers)
                    else: # No user with that auth token was found
                        #check that no other user has this token already
                        user = get_user_by_oauth_token(self.context, oauth_access_token)
                        if user and self.user != user:
                            raise Forbidden(_("Unable to Authenticate using OpenID"))

            controls = self.request.POST.items()
            try:
                appstruct = form.validate(controls)
            except ValidationFailure, e:
                self.response['form'] = e.render()
                return self.response
            
            name = appstruct['userid']
            del appstruct['userid']

            obj = createContent('User', creators=[name], **appstruct)
            self.context.users[name] = obj
            
            headers = remember(self.request, name) # login user
            
            url = resource_url(self.api.root, self.request)
            return HTTPFound(location=url, headers=headers)
                
        raise Forbidden(_("Unable to Authenticate using OpenID"))


@view_config(context=AuthenticationComplete, renderer="form_redirect.pt", permission=NO_PERMISSION_REQUIRED)
def cloud_login_complete(context, request):
    result = {
        'profile': context.profile,
        'credentials': context.credentials,
    }
    
    schema = createSchema('CSORegisterUserSchema').bind(context=context, request=request)
    add_csrf_token(context, request, schema)
    form = Form(schema, action='/cso', buttons=(button_register,))
    
    oauth_token = result['credentials']['oauthAccessToken']
    
    if 'preferredUsername' in result['profile']:
        userid = result['profile']['preferredUsername']
    elif 'displayName' in result['profile']:
        userid = result['profile']['displayName']
    if 'name' in result['profile']:
        first_name = result['profile']['name']['givenName']
        last_name = result['profile']['name']['familyName']
    else:
        first_name = ''
        last_name = ''
    if 'verifiedEmail' in result['profile']:
        email = result['profile']['verifiedEmail']
    else:
        email = ''
    if 'accounts' in result and len(result['accounts']) > 0:
        oauth_userid = result['accounts'][0]['userid']
        domain = result['accounts'][0]['domain']
    else:
        oauth_userid = ''
        domain = ''
        
    if not NEW_USERID_PATTERN.match(userid):
        userid = ''
    
    appstruct = {'userid': userid,
                'oauth_access_token': oauth_token, 
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'oauth_userid': oauth_userid,
                'domain': domain}
    
    return {'form': form.render(appstruct=appstruct)}

@view_config(context=AuthenticationDenied, permission=NO_PERMISSION_REQUIRED)
def cloud_login_denied(context, request):
    raise Forbidden(_("Unable to Authenticate using OpenID"))

def get_user_by_oauth_token(context, token):
    root = find_root(context)
    for user in root.users.get_content(iface=IUser):
        if user.get_field_value('oauth_access_token') == token:
            return user