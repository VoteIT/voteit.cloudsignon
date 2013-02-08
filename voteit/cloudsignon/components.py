from pyramid.renderers import render
from betahaus.viewcomponent import view_action
from velruse import login_url

from voteit.cloudsignon import VoteITCSO as _
from voteit.cloudsignon.fanstaticlib import voteit_cso 


def login_provider(context, request, va, **kw):
    voteit_cso.need()
    providers = request.registry.settings.get('login_providers', ())
    if va.name not in providers:
        return u""
    api = kw['api']
    response = dict(
        api = api,
        came_from = request.GET.get('came_from', ''),
        title = va.title,
    )   
    return render(va.kwargs['template'], response, request = request)

@view_action('login_forms', 'facebook', title = _(u"Facebook"), template="templates/facebook.pt")
@view_action('login_forms', 'twitter', title = _(u"Twitter"), template="templates/twitter.pt")
def login_va(context, request, va, **kw):
    api = kw['api']
    if not api.userid:
        return login_provider(context, request, va, **kw)
    return u""

@view_action('connect_forms', 'facebook', title = _(u"Connect to Facebook"), template="templates/facebook.pt")
@view_action('connect_forms', 'twitter', title = _(u"Connect to Twitter"), template="templates/twitter.pt")
def connect_va(context, request, va, **kw):
    api = kw['api']
    if api.userid and va.name not in api.user_profile.auth_domains:
        return login_provider(context, request, va, **kw)
    return u""  
