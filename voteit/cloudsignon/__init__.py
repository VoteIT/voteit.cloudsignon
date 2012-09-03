from pyramid.i18n import TranslationStringFactory


VoteITCSO = TranslationStringFactory('voteit.cloudsignon')

def includeme(config):
    config.scan('voteit.cloudsignon')
    config.include('voteit.cloudsignon.profile_image_plugins')
    config.add_translation_dirs('voteit.cloudsignon:locale/')
    
    # determine which providers we want to configure
    providers = config.registry.settings.get('login_providers', '')
    providers = filter(None, [p.strip()
                              for line in providers.splitlines()
                              for p in line.split(', ')])
    config.registry.settings['login_providers'] = providers
        
    if 'facebook' in providers:
        config.include('velruse.providers.facebook')
        config.add_facebook_login_from_settings(prefix='facebook.')

    if 'twitter' in providers:
        config.include('velruse.providers.twitter')
        config.add_twitter_login_from_settings(prefix='twitter.')
        
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('csostatic', 'voteit.cloudsignon:static', cache_max_age = cache_ttl_seconds)