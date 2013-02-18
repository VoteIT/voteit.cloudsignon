from pyramid.i18n import TranslationStringFactory

from voteit.core.models.interfaces import IUser
from voteit.core.models.interfaces import IProfileImage


VoteITCSO = TranslationStringFactory('voteit.cloudsignon')


def includeme(config):
    config.scan('voteit.cloudsignon')
    config.add_translation_dirs('voteit.cloudsignon:locale/')
    configure_providers(config)
    cache_ttl_seconds = int(config.registry.settings.get('cache_ttl_seconds', 7200))
    config.add_static_view('csostatic', 'voteit.cloudsignon:static', cache_max_age = cache_ttl_seconds)

def add_facebook(config, consumer_key, consumer_secret, **kw):
    from velruse.providers.facebook import add_facebook_login
    add_facebook_login(config, consumer_key, consumer_secret, **kw)
    from voteit.cloudsignon.profile_image_plugins import FacebookProfileImagePlugin
    config.registry.registerAdapter(FacebookProfileImagePlugin, (IUser,), IProfileImage, FacebookProfileImagePlugin.name)

def add_twitter(config, consumer_key, consumer_secret, **kw):
    from velruse.providers.twitter import add_twitter_login
    add_twitter_login(config, consumer_key, consumer_secret, **kw)
    from voteit.cloudsignon.profile_image_plugins import TwitterProfileImagePlugin
    config.registry.registerAdapter(TwitterProfileImagePlugin, (IUser,), IProfileImage, TwitterProfileImagePlugin.name)

def configure_providers(config):
    import ConfigParser
    from os.path import isfile

    provider_methods = {'facebook': add_facebook,
                        'twitter': add_twitter,}

    file_name = config.registry.settings.get('login_providers', 'etc/login_providers.ini')
    if not isfile(file_name):
        print u"CloudSignOn can't find any login providers file at: %s - won't add or configure any providers" % file_name
        return

    config.registry.settings['login_providers'] = []
    parser = ConfigParser.RawConfigParser()
    parser.read(file_name)
    sections = parser.sections()
    for section in parser.sections():
        consumer_key = parser.get(section, 'consumer_key')
        consumer_secret = parser.get(section, 'consumer_secret')
        provider_methods[section](config, consumer_key, consumer_secret)
        config.registry.settings['login_providers'].append(section)
        #FIXME: Add more options to config file
    if not sections:
        print u"CloudSignOn can't find any sections in file %s - can't configure any providers."
