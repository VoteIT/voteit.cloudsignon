from pyramid.renderers import render
from betahaus.viewcomponent import view_action
from velruse import login_url

from voteit.cloudsignon import VoteITCSO as _ 


@view_action('login_forms', 'cloudsignon')
def cloudsignon(context, request, va, **kw):
    response = {'api': kw['api'],
                'login_url': login_url,
                'providers': request.registry.settings['login_providers'],}
    
    return render('login.pt', response, request = request)