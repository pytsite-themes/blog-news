"""PytSite Blog News Theme
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def theme_load():
    from pytsite import package_info
    from plugins import assetman

    # Check for Blog application presence
    if package_info.name('app') != 'blog':
        raise RuntimeError('This theme is able to work only with PytSite Blog application. '
                           'See https://github.com/pytsite/blog for details.')

    # Assetman tasks
    assetman.t_js('**')
    assetman.t_copy_static('**')
    assetman.t_less('**')


def theme_load_wsgi():
    from pytsite import reg, tpl, router, events
    from plugins import assetman
    from . import controllers, eh

    # Home page route
    router.handle(controllers.Home, '/', 'home')

    # Following routes required by 'content' plugin as final point while processing request
    router.handle(controllers.ContentIndex, name='content_index')
    router.handle(controllers.ContentView, name='content_view')
    router.handle(controllers.ContentModify, name='content_modify')

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

    # Event handlers
    router.on_dispatch(eh.on_router_dispatch)
    tpl.on_render(eh.on_tpl_render)
    events.listen('settings@form.setup_widgets.theme', eh.settings_form_setup_widgets_setup_widgets_theme)

    # Preload permanent assets
    assetman.preload('twitter-bootstrap-3', True)
    assetman.preload('font-awesome', True)
    assetman.preload('common.js', True)

    # Force Twitter Bootstrap v3 on the password authentication page
    reg.put('auth_ui_password.twitter_bootstrap_version', 3)
