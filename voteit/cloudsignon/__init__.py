from pyramid.i18n import TranslationStringFactory


VoteITCSO = TranslationStringFactory('voteit.cloudsignon')

def includeme(config):
    config.scan('voteit.cloudsignon')
    config.add_translation_dirs('voteit.cloudsignon:locale/')
    
    # determine which providers we want to configure
    providers = config.registry.settings.get('login_providers', '')
    providers = filter(None, [p.strip()
                              for line in providers.splitlines()
                              for p in line.split(', ')])
    config.registry.settings['login_providers'] = providers
    if not any(providers):
        log.warn('no login providers configured, double check your ini '
                 'file and add a few')
        
    if 'facebook' in providers:
        config.include('velruse.providers.facebook')
        config.add_facebook_login_from_settings(prefix='facebook.')

    if 'twitter' in providers:
        config.include('velruse.providers.twitter')
        config.add_twitter_login_from_settings(prefix='twitter.')