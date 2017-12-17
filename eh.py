"""PytSite Blog News Theme Event Handlers
"""
from pytsite import lang, plugman, reg
from plugins import settings, widget, assetman

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def on_router_dispatch():
    assetman.preload('v{}/css/common.css'.format(reg.get('theme.version', '1')))


def on_tpl_render(tpl_name: str, args: dict):
    args.update({
        'theme_v': reg.get('theme.version', '1'),
        'top_navbar_items_num': int(reg.get('theme.top_navbar_items_num', '5')),
        'language_nav': widget.select.LanguageNav('language-nav'),
    })

    if plugman.is_installed(['page', 'section']):
        from plugins import content, section

        args['content_sections'] = list(section.get())

        if content.is_model_registered('page'):
            args['content_pages'] = list(content.find('page').get())


def settings_form_setup_widgets_setup_widgets_theme(frm: settings.Form):
    frm.add_widget(widget.select.Select(
        uid='setting_version',
        weight=100,
        label=lang.t('version'),
        items=[(str(i), lang.t('version_num', {'num': i})) for i in range(1, 4)],
        append_none_item=False,
        h_size='col-xs-12 col-sm-6 col-md-3',
    ))

    frm.add_widget(widget.select.Select(
        uid='setting_top_navbar_items_num',
        weight=110,
        label=lang.t('top_navbar_items_num'),
        items=[(str(i), str(i)) for i in range(1, 11)],
        append_none_item=False,
        h_size='col-xs-12 col-sm-1',
        default='5',
    ))
