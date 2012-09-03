from pyramid.renderers import render
from betahaus.viewcomponent import view_action
from velruse import login_url

from voteit.cloudsignon import VoteITCSO as _
from voteit.cloudsignon.fanstaticlib import voteit_cso 


@view_action('login_forms', 'cloudsignon')
def cloudsignon(context, request, va, **kw):
    voteit_cso.need()
    response = {'api': kw['api'],
                'login_url': login_url,
                'came_from': request.GET.get('came_from', ''),
                'providers': request.registry.settings['login_providers'],}
    
    return render('login.pt', response, request = request)

@view_action('connect_forms', 'cloudsignconnect')
def cloudsignconnect(context, request, va, **kw):
    voteit_cso.need()
    api = kw['api']
    user = api.user_profile
    response = {'api': api,
                'user': user,
                'login_url': login_url,
                'providers': request.registry.settings['login_providers'],}
    
    return render('connect.pt', response, request = request)