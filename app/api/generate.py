from markdown import Markdown
import os
import pypinyin
import pdb

INPUT_CONTENT = './app/blog/MD'
OUTPUT_CONTENT = './app/blog/HTML'

class generate(object):

    def __init__ (self):
        self._md_files = []
        self._md_file_path = INPUT_CONTENT
        self._current_file_index = None
        self._pinyin_names = set()
        self._output_content = ''

    def load_md_file(self, f_name):
        if os.path.splitext(f_name)[1].lower() == ".md":
            self._md_files.append(os.path.join(self._md_file_path, f_name))

    def load_all_md_files(self, folder):
        self._md_file_path = folder
        for root, dirs, files in os.walk(folder):
            for f in files:
                self.load_md_file(f)

    def gen_to_html(self, f_name):
        file_base_name = os.path.splitext(os.path.basename(f_name))[0]
        # self._current_file_index = self._str2pinyin(file_base_name)
        self._current_file_index = file_base_name
        self._pinyin_names.add(self._current_file_index)
        out_path = os.path.join(OUTPUT_CONTENT, self._current_file_index + ".html")
        html = self._render(f_name)
        self._save_html(out_path, html)

    def gen_all_to_html(self):
        for f in self._md_files:
            self.gen_to_html(f)

    def _str2pinyin(hans, style=pypinyin.FIRST_LETTER):
        pinyin_str = pypinyin.slug(hans, style=style, separator="")
        num = 2
        while pinyin_str in _pinyin_names:
            pinyin_str += str(num)
            num += 1
        return pinyin_str

    def _render(self, md_file):
        with open(md_file, "r") as f:
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
            html = md.convert(text)
            meta = md.Meta if hasattr(md, "Meta") else {}
            toc = md.toc if hasattr(md, "toc") else ""
            # create_index(md_file, meta)

            #template = env.get_template("base_article.html")
            '''
            text = template.render(
                blog_content=html
                """,
                static_root=STATIC_ROOT,
                title=ARTICLE_INDEX[_current_file_index].get("title"),
                title_html=render_title_html(ARTICLE_INDEX[_current_file_index].get("title")),
                summary=ARTICLE_INDEX[_current_file_index].get("summary", ""),
                authors=render_authors_html(ARTICLE_INDEX[_current_file_index].get("authors")),
                tags=render_tags_html(ARTICLE_INDEX[_current_file_index].get("tags")),
                toc=toc,
                """
            )
            '''

        return html

    def _save_html(self, out_path, html):
        base_folder = os.path.dirname(out_path)
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

        with open(out_path, 'w+') as f:
            f.write(html)
