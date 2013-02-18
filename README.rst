Cloud signon for VoteIT
=======================

Allow users to sign in or register with other providers. Currently Facebook and Twitter.


Usage
-----

Add a config file with login provider information, something like:

    [facebook]
    consumer_key = XXX
    consumer_secret = XXX
    
    [twitter]
    consumer_key = XXX
    consumer_secret = XXX

By default, this package expects the file to be in <buildout_dir>/etc/login_providers.
If you're not happy with that, simply add the option:

    login_providers = <filename>

to your paster config file.


Contacts
--------

Bugs, questions or anything else? Please see contant information on `www.voteit.se <http://www.voteit.se/>`_.
