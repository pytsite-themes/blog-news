"""Theme Controllers
"""
from datetime import datetime, timedelta
from pytsite import tpl, odm, settings, auth_profile, plugman, routing, assetman
from plugins import content, section, tag, comments
from app import model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Home(routing.Controller):
    """Home
    """

    def exec(self) -> str:
        theme_v = settings.get('current-theme.version', '1')
        exclude_ids = []

        starred = _get_articles(exclude_ids, 1, starred=True)

        tpl_args = {
            'page_header_article': starred[0] if starred else None,
            'page_header_article_tags': tag.widget.EntityTagCloud('header-article-tags', entity=starred[0],
                                                                  term_css='') if starred else None,
            'fullscreen_page_header': bool(starred),
        }

        if theme_v in ('1', '2'):
            sections = list(section.get())
            latest_by_section = {}
            for sec in sections:
                latest_by_section[sec.alias] = _get_articles(exclude_ids, 6, sec=sec)

            tpl_args.update({
                'sections': sections,
                'latest_articles_by_section': latest_by_section,
            })

        elif theme_v == '3':
            tpl_args.update({
                'latest_articles_first_left': _get_articles(exclude_ids, 4),
                'latest_articles_first_right': _get_articles(exclude_ids, 7, sort_field='views_count', days=7),
                'latest_articles_second_left': _get_articles(exclude_ids, 4),
                'latest_articles_second_right': _get_articles(exclude_ids, 7, sort_field='views_count', days=14),
            })

        assetman.preload('v{}/css/home.css'.format(theme_v))

        return tpl.render('v{}/home'.format(theme_v), tpl_args)


class ContentEntityIndex(routing.Controller):
    """Content entity index
    """

    def exec(self) -> str:
        theme_v = settings.get('current-theme.version', '1')

        self.args.update(content.paginate(self.arg('finder')))

        author = self.arg('author')
        if author:
            self.args['author_widget'] = auth_profile.widget.Profile('user-profile', user=author)

        assetman.preload('v{}/css/content-entity-index.css'.format(theme_v))

        return tpl.render('v{}/content-entity-index'.format(theme_v), self.args)


class ContentEntityView(routing.Controller):
    """Content entity view
    """

    def exec(self) -> str:
        theme_v = settings.get('current-theme.version', '1')
        e = self.arg('entity')
        exclude_ids = [e.id]

        self.args.update({
            'page_header_article': e,
            'page_header_article_tags': tag.widget.EntityTagCloud('header-article-tags', entity=e, term_css=''),
            'fullscreen_page_header': True,
            'entity_tags': tag.widget.EntityTagCloud('entity-tag-cloud', entity=e, term_css=''),
            'related_1': _get_articles(exclude_ids, 3, e.section, 'views_count') if e.model == 'article' else [],
            'related_2': _get_articles(exclude_ids, 2, e.section, 'views_count') if e.model == 'article' else [],
            'related_3': _get_articles(exclude_ids, 2, e.section) if e.model == 'article' else [],
        })

        if plugman.is_installed('addthis'):
            from plugins import addthis
            self.args.update({
                'share_widget': addthis.widget.AddThis('add-this-share') if settings.get('addthis.pub_id') else '',
            })

        if plugman.is_installed('disqus'):
            self.args.update({
                'comments_widget': comments.get_widget(driver_name='disqus')
            })

        assetman.preload('v{}/css/content-entity-view.css'.format(theme_v))

        return tpl.render('v{}/content-entity-view'.format(theme_v), self.args)


def _get_articles(exclude_ids: list, count: int = 6, sec: section.model.Section = None,
                  sort_field: str = 'publish_time', days: int = None, starred: bool = False) -> list:
    """Get articles
    """
    # Setup articles finder
    f = content.find('article').ninc('_id', exclude_ids).sort([(sort_field, odm.I_DESC)])

    # Filter by section
    if sec:
        f.eq('section', sec)

    # Filter by publish time
    if days:
        # Determine last published article date
        last_article = content.find('article').sort([('publish_time', odm.I_DESC)]).first()  # type: model.Article
        if last_article:
            f.gte('publish_time', last_article.publish_time - timedelta(days))
        else:
            f.gte('publish_time', datetime.now() - timedelta(days))

    # Filter by 'starred' flag
    if starred:
        f.eq('starred', True)

    r = []
    for article in f.get(count):
        # Show only articles which can be viewed by current user
        if article.odm_auth_check_permission('view') or article.odm_auth_check_permission('view_own'):
            r.append(article)
        exclude_ids.append(article.id)

    return r
