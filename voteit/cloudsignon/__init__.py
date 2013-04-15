from pyramid.i18n import TranslationStringFactory


VoteITCSO = TranslationStringFactory('voteit.cloudsignon')


def includeme(config):
    config.scan('voteit.cloudsignon')
    config.add_translation_dirs('voteit.cloudsignon:locale/')
    configure_providers(config)
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('csostatic', 'voteit.cloudsignon:static', cache_max_age = cache_ttl_seconds)

def add_facebook(config, **kw):
    """ Add Facebook login provider.
        requires consumer_key and consumer_secret in configuration.
    """
    from velruse.providers.facebook import add_facebook_login
    consumer_key = kw.pop('consumer_key')
    consumer_secret = kw.pop('consumer_secret')
    add_facebook_login(config, consumer_key, consumer_secret, **kw)
    from voteit.cloudsignon.profile_image_plugins import FacebookProfileImagePlugin
    config.registry.registerAdapter(FacebookProfileImagePlugin, name = FacebookProfileImagePlugin.name)

def add_twitter(config, **kw):
    """ Add Twitter login provider.
        requires consumer_key and consumer_secret in configuration.
    """
    from velruse.providers.twitter import add_twitter_login
    consumer_key = kw.pop('consumer_key')
    consumer_secret = kw.pop('consumer_secret')
    add_twitter_login(config, consumer_key, consumer_secret, **kw)
    from voteit.cloudsignon.profile_image_plugins import TwitterProfileImagePlugin
    config.registry.registerAdapter(TwitterProfileImagePlugin, name = TwitterProfileImagePlugin.name)

def add_openid(config, *args, **kw):
    """ Add OpenID login provider.
        requires realm to be used.
    """
    from velruse.providers.openid import add_openid_login
    realm = kw.pop('realm')
    if 'domain' in kw:
        domain = kw.pop('domain')
        config.registry.settings['openid_domain'] = domain
    add_openid_login(config, realm = realm, **kw)

def configure_providers(config):
    import ConfigParser
    from os.path import isfile

    provider_methods = {'facebook': add_facebook,
                        'twitter': add_twitter,
                        'openid': add_openid,}

    file_name = config.registry.settings.get('login_providers', 'etc/login_providers.ini')
    if not isfile(file_name):
        print u"CloudSignOn can't find any login providers file at: %s - won't add or configure any providers" % file_name
        return

    config.registry.settings['login_providers'] = []
    parser = ConfigParser.RawConfigParser()
    parser.read(file_name)
    sections = parser.sections()
    for section in parser.sections():
        kwargs = dict(parser.items(section))
        provider_methods[section](config, **kwargs)
        config.registry.settings['login_providers'].append(section)
    if not sections:
        print u"CloudSignOn can't find any sections in file %s - can't configure any providers."
