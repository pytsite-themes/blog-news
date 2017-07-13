"""PytSite Blog News Theme Settings Form
"""
from pytsite import settings, widget, lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Form(settings.Form):
    def _on_setup_widgets(self):
        self.add_widget(widget.select.Select(
            uid='setting_version',
            label=lang.t('version'),
            items=[(str(i), lang.t('version_num', {'num': i})) for i in range(1, 4)],
            append_none_item=False,
            h_size='col-xs-12 col-sm-6 col-md-3',
        ))

        self.add_widget(widget.select.Select(
            uid='setting_top_navbar_items_num',
            label=lang.t('top_navbar_items_num'),
            items=[(str(i), str(i)) for i in range(1, 11)],
            append_none_item=False,
            h_size='col-xs-12 col-sm-1',
            default='5',
        ))

        super()._on_setup_widgets()
