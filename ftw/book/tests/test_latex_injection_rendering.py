from ftw.book.interfaces import ILaTeXCodeInjectionEnabled
from ftw.book.interfaces import IWithinBookLayer
from ftw.book.testing import LATEX_ZCML_LAYER
from ftw.pdfgenerator.interfaces import IBuilder
from ftw.pdfgenerator.layout.baselayout import BaseLayout
from ftw.testing import MockTestCase
from zope.interface import directlyProvides


class TestInjectionAwareConvertObject(MockTestCase):

    layer = LATEX_ZCML_LAYER

    def setUp(self):
        super(TestInjectionAwareConvertObject, self).setUp()

        context = self.create_dummy()
        request = self.providing_stub(IWithinBookLayer)
        builder = self.providing_stub(IBuilder)

        self.layout = BaseLayout(context, request, builder)

    def mock_extender_values(self, mock, **data):
        default_data = {'preLatexCode': '',
                        'postLatexCode': ''}
        default_data.update(data)
        data = default_data

        schema = self.stub()
        self.expect(mock.Schema()).result(schema).count(0, None)

        for fieldname, value in data.items():
            self.expect(schema.getField(fieldname).get(mock)).result(value)

        return schema

    def test_not_injected_without_interface(self):
        obj = self.mocker.mock()
        self.expect(obj.Schema()).count(0)

        self.replay()

        self.assertEqual(self.layout.render_latex_for(obj), '')

    def test_injected_with_interface(self):
        latex_pre_code = 'INJECTED PRE LATEX CODE'
        latex_post_code = 'INJECTED POST LATEX CODE'

        obj = self.providing_stub(ILaTeXCodeInjectionEnabled)

        self.mock_extender_values(obj, preLatexCode=latex_pre_code,
                                  postLatexCode=latex_post_code)

        self.expect(obj.getPhysicalPath()).result(
            ['', 'myobj']).count(3)  # 3 = pre + post + assertion below

        self.replay()
        latex = self.layout.render_latex_for(obj)

        self.assertIn(latex_pre_code, latex)
        self.assertIn(latex_post_code, latex)
        self.assertIn('/'.join(obj.getPhysicalPath()), latex)

    def test_bad_schemaextender_state(self):
        # sometimes the field can not be retrieved. We do nothing and we
        # don't fail in this case.
        obj_dummy = self.create_dummy()
        directlyProvides(obj_dummy, ILaTeXCodeInjectionEnabled)
        obj = self.mocker.proxy(obj_dummy, spec=None)
        self.mock_extender_values(obj, preLatexCode=None)

        self.replay()
        latex = self.layout.render_latex_for(obj)

        self.assertEqual(latex.strip(), '')
