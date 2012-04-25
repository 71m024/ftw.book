from Products import DataGridField
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.Archetypes import atapi
from Products.Archetypes.public import DisplayList
from ftw.book import _
from ftw.book.config import PROJECTNAME
from ftw.book.interfaces import ITable
from ftw.book.table import generator
from zope.interface import implements
from simplelayout.base.interfaces import ISimpleLayoutBlock
from simplelayout.types.common.content import simplelayout_schemas


MAX_AMOUNT_OF_COLUMNS = 12
MAX_AMOUNT_OF_HEADER_ROWS = 5
MAX_AMOUNT_OF_FOOTER_ROWS = 5
BORDER_LAYOUTS = (
    ('grid', _(u'table_label_gridLayout', default=u'Grid Layout')),
    ('lines', _(u'table_label_linesLayout', default=u'Underline every row')),
    ('vertical', _(u'table_label_verticalLayout', default=u'Vertical grid')),
    )


table_schema = (ATContentTypeSchema.copy() + \
                   atapi.Schema((

            atapi.BooleanField(
                name='showTitle',
                schemata='default',
                default=False,
                widget=atapi.BooleanWidget(
                    label=_(u'label_show_title', default=u'Show title'),
                    description=_(u'description_show_title', default=u''),
                    ),
                ),

            DataGridField.DataGridField(
                name='data',
                schemata='default',
                searchable=False,
                required=False,
                columns=['column_%i' % i for i in
                         range(MAX_AMOUNT_OF_COLUMNS)] + ['row_format'],
                widget=DataGridField.DataGridWidget(
                    label=_(u'label_table_content', default=u'Table content'),
                    macro='datagridwidget_bibliothek_table',
                    columns=dict(
                        [
                            ('column_%i' % i, DataGridField.Column(
                                    label='%s %i' % (_('row'), i + 1)))
                            for i in range(MAX_AMOUNT_OF_COLUMNS)] + [(
                                'row_format',
                                DataGridField.SelectColumn(
                                    title='Format',
                                    vocabulary='getRowFormatVocabulary',
                                    ),
                                )]
                        ),
                    ),
                ),

            atapi.TextField(
                name='footnoteText',
                schemata='default',
                required=False,
                searchable=True,
                default_input_type='text/html',
                default_output_type='text/html',
                widget=atapi.RichWidget(
                    label=_(u'label_footnote_text', default=u'Footnote Text'),
                    description=_(u'description_footnote_text', default=u""),
                    ),
                ),

            DataGridField.DataGridField(
                name='columnProperties',
                schemata='Layout',
                searchable=False,
                required=False,
                allow_insert=False,
                allow_delete=False,
                allow_reorder=False,
                columns=(
                    'columnId',
                    'columnTitle',
                    'active',
                    'alignment',
                    'bold',
                    'indent',
                    'width',
                    ),
                widget=DataGridField.DataGridWidget(
                    label=_(u'label_column_properties',
                        default=u'Column properties'),
                    columns={
                        'columnId': DataGridField.FixedColumn(
                            'column_id',
                            default='column_x',
                            visible=False,
                            ),
                        'columnTitle': DataGridField.FixedColumn(
                            _(u'table_label_column', default=u'Column'),
                            default='Row X',
                            ),
                        'active': DataGridField.CheckboxColumn(
                            _(u'table_label_active', default=u'Active'),
                            default=False,
                            ),
                        'alignment': DataGridField.SelectColumn(
                            _(u'table_label_alignment', default=u'Alignment'),
                            vocabulary='getAlignmentVocabulary',
                            ),
                        'bold': DataGridField.CheckboxColumn(
                            _(u'table_label_bold', default=u'Bold'),
                            default=False,
                            ),
                        'indent': DataGridField.SelectColumn(
                            _(u'table_label_indent', default=u'Indent'),
                            vocabulary='getIndentVocabulary',
                            ),
                        'width': DataGridField.Column(
                            label=_(u'table_label_width',
                                      default=u'Width (%)'),
                            ),
                        },
                    ),
                fixed_rows=[
                    DataGridField.FixedRow(
                        keyColumn='columnId',
                        initialData={
                            'columnId':'column_%i' % (i),
                            'columnTitle': 'Spalte %i' % (i + 1),
                            'active': False,
                            'alignment': '',
                            'bold': False,
                            'indent': '',
                            },
                        ) for i in range(MAX_AMOUNT_OF_COLUMNS)],
                ),

            atapi.StringField(
                name='headerRows',
                schemata='Layout',
                default='1',
                enforceVocabulary=True,
                vocabulary=[
                    (str(i), '%i %s' % (i, _('rows'))) for i
                    in range(MAX_AMOUNT_OF_HEADER_ROWS + 1)],
                widget=atapi.SelectionWidget(
                    label=_(u'label_header_rows',
                        default=u'Amount of header rows'),
                    description=_(u'description_header_row',
                        default=u''),
                    ),
                ),

            atapi.StringField(
                name='footerRows',
                schemata='Layout',
                default=0,
                enforceVocabulary=True,
                vocabulary=[
                    (str(i), '%i %s' % (i, _('rows'))) for i
                    in range(MAX_AMOUNT_OF_FOOTER_ROWS+1)],
                widget=atapi.SelectionWidget(
                    label=_(u'label_footer_rows',
                        default=u'Amount of footer rows'),
                    description=_(u'description_footer_row',
                        default=u''),
                    ),
                ),

            atapi.BooleanField(
                name='firstColumnIsHeader',
                schemata='Layout',
                default=False,
                widget=atapi.BooleanWidget(
                    label=_(u'label_first_column_is_header',
                        default=u'First column is a header column'),
                    description=_(u'description_first_column_is_header',
                        default=u''),
                    ),
                ),

            atapi.BooleanField(
                name='headerIsBold',
                schemata='Layout',
                default=True,
                widget=atapi.BooleanWidget(
                    label=_(u'label_header_is_bold',
                        u'Header rows are bold'),
                    description=_(u'description_header_is_bold',
                        default=''),
                    ),
                ),

            atapi.BooleanField(
                name='footerIsBold',
                schemata='Layout',
                default=True,
                widget=atapi.BooleanWidget(
                    label=_(u'label_footer_is_bold',
                        u'Footer rows are bold'),
                    description=_(u'description_footer_is_bold',
                        default=''),
                    ),
                ),

            atapi.StringField(
                name='borderLayout',
                schemata='Layout',
                default='lines',
                enforceVocabulary=True,
                vocabulary=BORDER_LAYOUTS,
                widget=atapi.SelectionWidget(
                    label=_(u'label_border_layout', default=u'Border Layout'),
                    description=_(u'description_border_layout', default=u''),
                    )
                ),

            atapi.BooleanField(
                name='noLifting',
                schemata='Layout',
                default=False,
                widget=atapi.BooleanWidget(
                    label=_(u'label_no_lifting', default=u'No lifting'),
                    description=_(u'description_no_lifting', default=u''),
                    )),

            )))

# We need a text-field if we inherit from ATDocumentBase
table_schema += simplelayout_schemas.textSchema.copy()
table_schema['text'].widget.visible = {'edit': 0, 'view': 0}

simplelayout_schemas.finalize_simplelayout_schema(table_schema)


class Table(ATDocumentBase):
    """A Table for ftw.book"""
    implements(ITable, ISimpleLayoutBlock)

    portal_type = "Table"
    schema = table_schema

    def getTable(self):
        return generator.TableGenerator(self).render()

    def convert_to_int(self, value):
        """ Converts a value to integer. If its not possible we return the
        unconverted value
        """
        try:
            return int(value)
        except ValueError:
            return value

    def getHeaderRows(self, as_int=False):
        """ We need to calculate with the keys of the headerRows. So we need
        integers. But the vocabulary of a ATField needs strings as keys.
        """
        if as_int:
            return self.convert_to_int(self.headerRows)
        return self.headerRows

    def getFooterRows(self, as_int=False):
        """ We need to calculate with the keys of the footerRsows. So we need
        integers. But the vocabulary of a ATField needs strings as keys.
        """
        if as_int:
            return self.convert_to_int(self.footerRows)
        return self.footerRows

    def getAlignmentVocabulary(self):
        return DisplayList((
                ('', _('automatically')),
                ('left', _('left')),
                ('right', _('right')),
                ('center', _('center')),
                ))

    def getIndentVocabulary(self):
        return DisplayList((
                ('', _('no indent')),
                ('indent2', _('2mm')),
                ('indent10', _('10mm')),
                ))

    def getRowFormatVocabulary(self):
        return DisplayList((
                ('', _('Normal')),
                ('bold', _('Bold')),
                ('indent2', _('2mm indent')),
                ('indent10', _('10mm indent')),
                ('indent2 bold', _('2mm ind. + bold')),
                ('indent10 bold', _('10mm ind. + bold')),
                ('noborders', _('Row without line')),
                ('grey', _('Grey font')),
                ('scriptsize', _('Small font')),
                ('fullColspan', _('Strech first line')),
                ))

atapi.registerType(Table, PROJECTNAME)
