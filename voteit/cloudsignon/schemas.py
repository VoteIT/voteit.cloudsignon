import colander
import deform
from betahaus.pyracont.decorators import schema_factory

from voteit.core.schemas.user import userid_node
from voteit.core.schemas.user import email_node
from voteit.core.schemas.user import first_name_node
from voteit.core.schemas.user import last_name_node
from voteit.core.schemas.user import came_from_node

from voteit.cloudsignon import VoteITCSO as _

    
@schema_factory('CSORegisterUserSchema',
                title = _(u"Registration"),
                description=_(u"cso_complete_registration_notice",
                              default = u'Review or complete your registration below.'))
class CSORegisterUserSchema(colander.Schema):
    """ CSO registration. """
    userid = userid_node()
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
