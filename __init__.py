"""PytSite Blog News Theme
"""
from pytsite import tpl, assetman, settings, package_info, plugman, router, widget
from . import settings_form

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Check for Blog application presence
if package_info.name('app') != 'blog':
    raise RuntimeError('This theme is able to work only with PytSite Blog application. '
                       'See https://github.com/pytsite/blog for details.')


def on_router_dispatch():
    assetman.preload('v{}/css/common.css'.format(settings.get('current-theme.version', '1')))


def on_tpl_render(tpl_name: str, args: dict):
    args.update({
        'theme_v': settings.get('current-theme.version', '1'),
        'top_navbar_items_num': int(settings.get('current-theme.top_navbar_items_num', '5')),
        'language_nav': widget.select.LanguageNav('language-nav'),
    })

    if plugman.is_installed(['page', 'section']):
        from plugins import content, section

        args['content_sections'] = list(section.get())

        if content.is_model_registered('page'):
            args['content_pages'] = list(content.find('page').get())


# Assetman tasks
assetman.t_js('**')
assetman.t_copy_static('**')
assetman.t_less('**')

# Preload permanent assets
assetman.preload('twitter-bootstrap', True)
assetman.preload('font-awesome', True)
assetman.preload('common.js', True)

# Theme settings form
settings.define('current-theme', settings_form.Form, 'theme', 'fa fa-globe', 'pytsite.theme.manage')

# Event handlers
router.on_dispatch(on_router_dispatch)
tpl.on_render(on_tpl_render)

if plugman.is_installed(['content', 'section', 'article', 'page']):
    from plugins import content, section
    from . import controllers

    router.handle(controllers.Home(), '/', 'home')

    # Following routes required by 'content' plugin as final point while processing request
    router.handle(controllers.ContentEntityIndex(), name='content_entity_index')
    router.handle(controllers.ContentEntityView(), name='content_entity_view')
    router.handle(controllers.ContentEntityModify(), name='content_entity_modify')

    # "Article index by section" route
    router.handle('content@index', '/section/<term_alias>', 'article_index_by_section', {
        'model': 'article',
        'term_field': 'section',
    })

    # "Article index by tag" route
    router.handle('content@index', '/tag/<term_alias>', 'article_index_by_tag', {
        'model': 'article',
        'term_field': 'tags',
    })

    # "Article index by author" route
    router.handle('content@index', '/author/<author>', 'article_index_by_author', {
        'model': 'article',
    })
