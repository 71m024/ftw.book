from AccessControl import ClassSecurityInfo
from Products.ATContentTypes import ATCTMessageFactory as _at
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.Archetypes import atapi
from ftw.book.config import PROJECTNAME
from ftw.book.interfaces import IRemark
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.types.common.content import simplelayout_schemas
from zope.i18nmessageid import MessageFactory
from zope.interface import implements


_sl = MessageFactory('simplelayout')


remark_schema = ATContentTypeSchema.copy()

remark_schema += atapi.Schema((

        atapi.BooleanField(
            name='showTitle',
            schemata='default',
            default=False,

            widget=atapi.BooleanWidget(
                label=_sl(u'simplelayout_label_showtitle',
                          default=u'Show Title'),
                description=_sl(u'simplelayout_help_showtitle',
                                default=u'Show title'))),

        ))

remark_schema += simplelayout_schemas.textSchema.copy()

remark_schema['text'].widget = atapi.TextAreaWidget(
    label=_at(u'label_body_text', default=u'Body Text'),
    description='',
    rows=32,
    cols=70)

remark_schema['title'].required = False
remark_schema['title'].searchable = 0
remark_schema['excludeFromNav'].default = True
remark_schema['description'].widget.visible = {'edit': 0, 'view': 0}
simplelayout_schemas.finalize_simplelayout_schema(remark_schema)


class Remark(ATDocumentBase):
    """A simplelayout block used for comments
    """

    security = ClassSecurityInfo()
    implements(IRemark, ISimpleLayoutBlock)
    schema = remark_schema


atapi.registerType(Remark, PROJECTNAME)
