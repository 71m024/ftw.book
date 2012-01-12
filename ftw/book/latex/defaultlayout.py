from Acquisition import aq_inner, aq_parent
from Products.Archetypes import atapi
from Products.Archetypes import public
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from ftw.book import _
from ftw.book.interfaces import IBook
from ftw.book.latex.layouts import register_book_layout
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.layout.makolayout import MakoLayoutBase
from zope.component import adapts
from zope.interface import implements, Interface


class StringField(ExtensionField, public.StringField):
    pass


class TextField(ExtensionField, public.TextField):
    pass


class IDefaultBookLayoutSelectionLayer(Interface):
    """Request layer interface for selecting the default book layout.
    """

register_book_layout(IDefaultBookLayoutSelectionLayer,
                     _(u'Default layout'))


class DefaultBookLayoutExtender(object):
    """Schema extender, adding the layout-specific fields "release", "author"
    and "author_address" to the book when the default layout is selected.
    """

    adapts(IBook)
    implements(ISchemaExtender)

    fields = [
        StringField(
            name='release',
            default='',
            required=False,
            widget=atapi.StringWidget(
                label=_(u'book_label_release', default=u'Release'),
                description=_(u'book_help_release', default=u''))),

        StringField(
            name='author',
            default='',
            required=False,
            widget=atapi.StringWidget(
                label=_(u'book_label_author', default=u'Author'),
                description=_(u'book_help_author', default=u''))),

        TextField(
            name='author_address',
            default='',
            required=False,
            default_content_type='text/plain',
            allowable_content_types=('text/plain',),
            default_output_type='text/plain',

            widget=atapi.TextAreaWidget(
                label=_(u'book_label_author_address',
                        default=u'Author Address'),
                description=_(u'book_help_author_address',
                              default=u''))),
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        request = self.context.REQUEST
        if IDefaultBookLayoutSelectionLayer.providedBy(request):
            return self.fields
        else:
            return []


class DefaultBookLayout(MakoLayoutBase):
    """A default book layout based on sphinx layout.
    """

    adapts(Interface, IDefaultBookLayoutSelectionLayer, IBuilder)

    template_directories = ['default_layout_templates']
    template_name = 'main.tex'

    def get_render_arguments(self):
        book = self.get_book()

        convert = self.get_converter().convert

        address = book.Schema().getField('author_address').get(book)
        address = convert(address.replace('\n', '<br />')).replace('\n', '')

        args = {
            'context_is_book': self.context == book,
            'title': convert(book.Title()),
            'use_titlepage': book.getUse_titlepage(),
            'use_toc': book.getUse_toc(),
            'use_lot': book.getUse_lot(),
            'use_loi': book.getUse_loi(),
            'release': convert(book.Schema().getField('release').get(book)),
            'author': convert(book.Schema().getField('author').get(book)),
            'authoraddress': address,
            # XXX: how to use in this layout?
            # 'pagestyle': book.getPagestyle(),
            }
        return args

    def get_book(self):
        obj = self.context
        while obj and not IBook.providedBy(obj):
            obj = aq_parent(aq_inner(obj))
        return obj

    def before_render_hook(self):
        self.use_package('inputenc', options='utf8', append_options=False)
        self.use_package('fontenc', options='T1', append_options=False)
        self.use_package('babel')
        self.use_package('times')
        self.use_package('fncychap', 'Sonny', append_options=False)
        self.use_package('longtable')
        self.use_package('sphinx')

        self.add_raw_template_file('sphinx.sty')
        self.add_raw_template_file('fncychap.sty')
        self.add_raw_template_file('sphinxftw.cls')
        self.add_raw_template_file('sphinxhowto.cls')
        self.add_raw_template_file('sphinxmanual.cls')