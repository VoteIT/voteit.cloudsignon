import colander
import deform
from betahaus.pyracont.decorators import schema_factory

from voteit.core.validators import deferred_new_userid_validator
from voteit.core.schemas.user import userid_preparer
from voteit.core.schemas.user import password_node
from voteit.core.schemas.user import email_node
from voteit.core.schemas.user import first_name_node
from voteit.core.schemas.user import last_name_node
from voteit.core.schemas.user import came_from_node

from voteit.cloudsignon import VoteITCSO as _
from voteit.cloudsignon.validators import deferred_unique_oauth_access_token_validator

def oauth_access_token_node():
    return colander.SchemaNode(colander.String(),
                               widget = deform.widget.HiddenWidget(),
                               validator=deferred_unique_oauth_access_token_validator,)
    
@schema_factory('CSORegisterUserSchema', title = _(u"Registration"))
class CSORegisterUserSchema(colander.Schema):
    """ CSO registration. """
    userid = colander.SchemaNode(colander.String(),
                                 title = _(u"UserID"),
                                 description = _('userid_description',
                                                 default=u" Used as a nickname, in @-links and as a unique id. You can't change this later. OK characters are: a-z, 0-9, '.', '-', '_'."),
                                 validator=deferred_new_userid_validator,
                                 preparer=userid_preparer,)
    email = email_node()
    first_name = first_name_node()
    last_name = last_name_node()
    oauth_access_token = oauth_access_token_node();