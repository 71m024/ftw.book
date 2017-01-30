from ftw.book.interfaces import IChapter
from ftw.simplelayout.interfaces import ISimplelayoutContainerConfig
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISimplelayoutContainerConfig)
@adapter(IChapter, Interface)
class ChapterConfigAdapter(object):

    def __init__(self, context, request):
        pass

    def __call__(self, settings):
        settings['layouts'] = []

    def default_page_layout(self):
        return {'default': [{"cols": [{"blocks": []}]}]}