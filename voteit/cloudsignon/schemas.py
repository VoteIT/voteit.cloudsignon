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

    
@schema_factory('CSORegisterUserSchema', title = _(u"Registration"), description=_('You must complete the form below with the required information to use VoteIT.'))
class CSORegisterUserSchema(colander.Schema):
    """ CSO registration. """
    userid = colander.SchemaNode(colander.String(),
                                 title = _(u"UserID"),
                                 description = _('userid_description',
                                                 default=u" Used as a nickname, in @-links and as a unique id. You can't change this later. OK characters are: a-z, 0-9, '.', '-', '_'."),
                                 validator=deferred_new_userid_validator,)
    email = email_node()
    first_name = first_name_node()
    last_name = last_name_node()
    domain = colander.SchemaNode(colander.String(),
                                 widget = deform.widget.HiddenWidget(),
                                 missing=u"",)
    oauth_access_token = colander.SchemaNode(colander.String(),
                                             widget = deform.widget.HiddenWidget(),)
    oauth_userid = colander.SchemaNode(colander.String(),
                                       widget = deform.widget.HiddenWidget(),
                                       missing=u"",)
    came_from = came_from_node()