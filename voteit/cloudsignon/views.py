import colander
import json
import urllib

from betahaus.pyracont.factories import createContent
from betahaus.pyracont.factories import createSchema
from deform import Form
from deform.exception import ValidationFailure
from pyramid.exceptions import Forbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.security import remember
from pyramid.traversal import find_root
from pyramid.url import resource_url
from pyramid.view import view_config
from velruse.providers import twitter
from velruse.providers import facebook
from velruse import AuthenticationComplete
from velruse import AuthenticationDenied
from velruse import login_url
from httplib2 import Http
from urllib import urlencode

from voteit.core.models.interfaces import ISiteRoot
from voteit.core.models.interfaces import IUser
from voteit.core.views.base_edit import BaseEdit
from voteit.core.models.schemas import add_csrf_token
from voteit.core.models.schemas import button_register
from voteit.core.models.schemas import button_cancel
from voteit.core.validators import NEW_USERID_PATTERN

from voteit.cloudsignon import VoteITCSO as _


class CloudSignOnView(BaseEdit):        
    
    @view_config(context=ISiteRoot, name='facebook_register', renderer="voteit.core.views:templates/base_edit.pt", permission=NO_PERMISSION_REQUIRED)
    def facebook_register(self):
        
        schema = createSchema('CSORegisterUserSchema').bind(context=self.context, request=self.request)
        add_csrf_token(self.context, self.request, schema)
        form = Form(schema, buttons=(button_register,button_cancel,))
        self.api.register_form_resources(form)
        
        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(_(u"Canceled"))

            url = resource_url(self.api.root, self.request)
            return HTTPFound(location=url)

        if self.request.POST:
            post = dict(self.request.POST)
            
            oauth_userid = post['oauth_userid']
            oauth_access_token = post['oauth_access_token']
            
            came_from = post['came_from']
            
            # Logged in user, connect auth token to user
            if self.api.userid:
                user = self.api.user_profile
                
                #check that no other user has this token already
                other_user = self.api.root.users.get_user_by_oauth_token('facebook', oauth_access_token)
                if other_user and user != other_user:
                    raise Forbidden(_("Another user has already registered with this token."))
                
                #setting domain stuff
                user.auth_domains['facebook'] = {'oauth_userid': oauth_userid, 
                                                 'oauth_access_token': oauth_access_token,}
                url = resource_url(user, self.request)
                return HTTPFound(location=url)
            else:
                # Find user with auth token and log it in
                user = self.api.root.users.get_user_by_oauth_token('facebook', oauth_access_token)
                if user:
                    if IUser.providedBy(user):
                        headers = remember(self.request, user.__name__)
                        url = resource_url(self.context, self.request)
                        if came_from:
                            url = urllib.unquote(came_from)
                        return HTTPFound(location = url,
                                         headers = headers)
            
    
            if 'register' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except ValidationFailure, e:
                    self.response['form'] = e.render()
                    return self.response
                
                name = appstruct['userid']
                del appstruct['userid']
                
                # removing domain data from appstruct
                del appstruct['oauth_userid']
                del appstruct['oauth_access_token']
                
                # add facebook as selected profile image
                appstruct['profile_image_plugin'] = 'facebook_profile_image'
                
                del appstruct['came_from']
    
                obj = createContent('User', creators=[name], **appstruct)
                self.context.users[name] = obj
                #setting domain stuff
                obj.auth_domains['facebook'] = {'oauth_userid': oauth_userid,
                                                 'oauth_access_token': oauth_access_token,}
                
                headers = remember(self.request, name) # login user
                
                url = resource_url(self.api.root, self.request)
                if came_from:
                    url = urllib.unquote(came_from)
                return HTTPFound(location=url, headers=headers)
            else:
                self.response['form'] = form.render(self.request.POST)
                return self.response
                
        raise Forbidden(_("Unable to authenticate using Facebook"))
    
    @view_config(context=ISiteRoot, name='twitter_register', renderer="voteit.core.views:templates/base_edit.pt", permission=NO_PERMISSION_REQUIRED)
    def twitter_register(self):
        
        schema = createSchema('CSORegisterUserSchema').bind(context=self.context, request=self.request)
        add_csrf_token(self.context, self.request, schema)
        form = Form(schema, buttons=(button_register,button_cancel,))
        self.api.register_form_resources(form)
        
        if 'cancel' in self.request.POST:
            self.api.flash_messages.add(_(u"Canceled"))

            url = resource_url(self.api.root, self.request)
            return HTTPFound(location=url)

        if self.request.POST:
            post = dict(self.request.POST)
            
            oauth_userid = post['oauth_userid']
            oauth_access_token = post['oauth_access_token']
            display_name = post['userid']
            
            came_from = post['came_from']
            
            # Logged in user, connect auth token to user
            if self.api.userid:
                user = self.api.user_profile
                
                #check that no other user has this token already
                other_user = self.api.root.users.get_user_by_oauth_token('twitter', oauth_access_token)
                if other_user and user != other_user:
                    raise Forbidden(_("Another user has already registered with this token."))
                
                #setting domain stuff
                user.auth_domains['twitter'] = {'oauth_userid': oauth_userid,
                                                'oauth_access_token': oauth_access_token,
                                                'display_name': display_name,}
                url = resource_url(user, self.request)
                return HTTPFound(location=url)
            else:
                # Find user with auth token and log it in
                user = self.api.root.users.get_user_by_oauth_token('twitter', oauth_access_token)
                if user:
                    if IUser.providedBy(user):
                        headers = remember(self.request, user.__name__)
                        url = resource_url(self.context, self.request)
                        if came_from:
                            url = urllib.unquote(came_from)
                        return HTTPFound(location = url,
                                         headers = headers)

            if 'register' in self.request.POST:
                controls = self.request.POST.items()
                try:
                    appstruct = form.validate(controls)
                except ValidationFailure, e:
                    self.response['form'] = e.render()
                    return self.response
                
                name = appstruct['userid']
                del appstruct['userid']
                
                # removing domain data from appstruct
                del appstruct['oauth_userid']
                del appstruct['oauth_access_token']
                
                # add twitter as selected profile image
                appstruct['profile_image_plugin'] = 'twitter_profile_image'
                
                del appstruct['came_from']
    
                obj = createContent('User', creators=[name], **appstruct)
                self.context.users[name] = obj
                #setting domain stuff
                obj.auth_domains['twitter'] = {'oauth_userid': oauth_userid,
                                               'oauth_access_token': oauth_access_token,
                                               'display_name': display_name,}
                
                headers = remember(self.request, name) # login user
                
                url = resource_url(self.api.root, self.request)
                if came_from:
                    url = urllib.unquote(came_from)
                return HTTPFound(location=url, headers=headers)
            else:
                self.response['form'] = form.render(self.request.POST)
                return self.response
                
        raise Forbidden(_("Unable to authenticate using Twitter"))

@view_config(context=ISiteRoot, name='facebook_login', permission=NO_PERMISSION_REQUIRED)
def facebook_login(self, request):
    if request.POST:
        request.session['came_from'] = request.POST.get('came_from', '') 
        provider = request.registry.velruse_providers['facebook']
        return provider.login(request)
    
    return HTTPBadRequest()
    
@view_config(context=ISiteRoot, name='twitter_login', permission=NO_PERMISSION_REQUIRED)
def twitter_login(self, request):
    if request.POST:
        request.session['came_from'] = request.POST.get('came_from', '')
        provider = request.registry.velruse_providers['twitter']
        return provider.login(request)
    
    return HTTPBadRequest() 

@view_config(context=facebook.FacebookAuthenticationComplete, renderer="form_redirect.pt", permission=NO_PERMISSION_REQUIRED)
def facebook_login_complete(context, request):
    result = {
        'profile': context.profile,
        'credentials': context.credentials,
    }
    
    schema = createSchema('CSORegisterUserSchema').bind(context=context, request=request)
    add_csrf_token(context, request, schema)
    form = Form(schema, action='/facebook_register', buttons=(button_register,))
    
    oauth_token = result['credentials']['oauthAccessToken']
    oauth_userid = result['profile']['accounts'][0]['userid']
    
    if 'preferredUsername' in result['profile']:
        userid = result['profile']['preferredUsername']
    else:
        userid = ''
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
        
    if not NEW_USERID_PATTERN.match(userid):
        userid = ''
    
    appstruct = {'userid': userid,
                'oauth_access_token': oauth_token, 
                'oauth_userid': oauth_userid,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,}
    appstruct['came_from'] = request.session.get('came_from', '')
    del request.session['came_from']
    
    return {'form': form.render(appstruct=appstruct)}

@view_config(context=twitter.TwitterAuthenticationComplete, renderer="form_redirect.pt", permission=NO_PERMISSION_REQUIRED)
def twitter_login_complete(context, request):
    result = {
        'profile': context.profile,
        'credentials': context.credentials,
    }
    
    schema = createSchema('CSORegisterUserSchema').bind(context=context, request=request)
    add_csrf_token(context, request, schema)
    form = Form(schema, action='/twitter_register', buttons=(button_register,))
    
    oauth_token = result['credentials']['oauthAccessToken']
    oauth_userid = result['profile']['accounts'][0]['userid']
    
    if 'displayName' in result['profile']:
        userid = result['profile']['displayName']
    else:
        userid = ''
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
        
    if not NEW_USERID_PATTERN.match(userid):
        userid = ''
    
    appstruct = {'userid': userid,
                'oauth_access_token': oauth_token, 
                'oauth_userid': oauth_userid,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,}
    appstruct['came_from'] = request.session.get('came_from', '')
    del request.session['came_from']
    
    return {'form': form.render(appstruct=appstruct)}


@view_config(context=AuthenticationDenied, permission=NO_PERMISSION_REQUIRED)
def cloud_login_denied(context, request):
    del request.session['came_from']
    raise Forbidden(_("Unable to Authenticate"))