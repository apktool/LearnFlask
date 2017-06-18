import codecs
from markdown import Markdown
from jinja2 import Environment, FileSystemLoader
from os.path import basename, splitext
import pdb

env = Environment(
    loader=FileSystemLoader("./app/templates")
)


class render(object):
    def __init__(self, f_name):
        self.article_index = {}
        self.tag_inverted_index = {}
        self.author_inverted_index = {}
        self._current_file = f_name
        self._current_file_index=splitext(basename(f_name))[0]

        self._body_html_template = 'base_article.html'
        self._title_html_template = u"<div class='sidebar-module-inset'><h5 class='sidebar-title'><i class='icon-circle-blank side-icon'></i>标题</h5><p>{title_str}</p></div>"
        self._author_html_template = u"<a href='/user/{author}' class='tag-index'>{author}</a>"
        self._tag_html_template = u"<a href='/tag/{tag}' class='tag-index'>{tag}</a>"

    def render_to_html(self):
        """渲染html页面
        :param md_file:
        :return:
        """
        with codecs.open(self._current_file, "r", "utf-8") as f:
            text = f.read()
            md = Markdown(
                extensions=[
                    "fenced_code",
                    "codehilite(css_class=highlight,linenums=None)",
                    "meta",
                    "admonition",
                    "tables",
                    "toc",
                    "wikilinks",
                ],
            )
            meta = {}
            meta['text'] = md.convert(text)
            meta['meta'] = md.Meta if hasattr(md, "Meta") else {}
            meta['toc'] = md.toc if hasattr(md, "toc") else ""
            # generate_index.create_index(md_file, meta)

            template = env.get_template(self._body_html_template)
            meta['html'] = template.render(
                blog_content=meta['text'],
                # static_root=STATIC_ROOT,
                summary=meta['meta'].get('summary')[0],
                title=meta['meta'].get('title')[0],

                title_html=self._render_title_html(meta['meta'].get('title')[0]),
                authors=self._render_authors_html(meta['meta'].get('authors')),
                tags=self._render_tags_html(meta['meta'].get('tags')),
                toc=meta['toc'],
            )

        return meta

    def _render_title_html(self, title):
        """渲染标题html
        """
        title_html = ""
        if title.strip() != "":
            title_html = self._title_html_template.format(title_str=title)
        return title_html

    def _render_authors_html(self, authors):
        """渲染作者html
        """
        authors_html = ""
        for author in authors:
            authors_html += self._author_html_template.format(author=author)
        return authors_html

    def _render_tags_html(self, tags):
        """渲染tags的html
        """
        tags_html = ""
        for tag in tags:
            tags_html += self._tag_html_template.format(tag=tag)
        return tags_html
