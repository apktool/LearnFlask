from flask_login import current_user
from datetime import datetime
from ..models import Post
from .. import db
import os
import pdb
import shutil
import shelve
import pypinyin

INPUT_CONTENT = './app/blog/MD'
OUTPUT_CONTENT = './app/blog/HTML'
OUT_CONTENT = './app/blog/OUT/'
INDEX_DAT = './app/blog/OUT/index.dat'

# 文章索引
ARTICLE_INDEX = {}
# 标签倒排索引
TAG_INVERTED_INDEX = {}
# 作者倒排索引
AUTHOR_INVERTED_INDEX = {}


class generate_html(object):

    def __init__(self, meta):
        self._md_files = []
        self._md_file_path = INPUT_CONTENT
        self._current_file_index = None
        self._pinyin_names = set()
        self._output_content = ''
        self._save_type = {}
        self.meta = meta

    def load_md_file(self, f_name):
        if os.path.splitext(f_name)[1].lower() == ".md":
            self._md_files.append(f_name)

    def load_all_md_files(self, folder):
        self._md_file_path = folder
        for root, dirs, files in os.walk(folder):
            for f in files:
                self.load_md_file(f)

    def gen_to_html(self, f_name):
        f_name = os.path.join(self._md_file_path, f_name)
        file_base_name = os.path.splitext(os.path.basename(f_name))[0]
        # self._current_file_index = self._str2pinyin(file_base_name)
        self._current_file_index = file_base_name
        self._pinyin_names.add(self._current_file_index)

        self._save_type['html'] = self.meta.get('html')

        # self._render(f_name)
        self._save_html_text()

    def gen_all_to_html(self):
        for f in self._md_files:
            self.gen_to_html(f)

    def _str2pinyin(self, hans, style=pypinyin.FIRST_LETTER):
        pinyin_str = pypinyin.slug(hans, style=style, separator="")
        num = 2
        while pinyin_str in self._pinyin_names:
            pinyin_str += str(num)
            num += 1
        return pinyin_str

    def _save_html_text(self):
        md_path = os.path.join(INPUT_CONTENT, self._current_file_index + ".md")
        html_path = os.path.join(OUTPUT_CONTENT, self._current_file_index + ".html")

        with open(md_path, "r") as f:
            self._save_type['text'] = f.read()

        with open(html_path, 'w+') as f:
            f.write(self._save_type['html'])

        post = Post(body=self._save_type['text'], body_html=self._save_type['html'], author=current_user._get_current_object())
        db.session.add(post)

    def clean(self):
        if os.path.exists(OUT_CONTENT):
            shutil.rmtree(OUT_CONTENT)


class generate_index(object):
    def __init__(self, meta):
        self.meta = meta.get('meta')

    def drop_index(self):
        global TAG_INVERTED_INDEX, ARTICLE_INDEX, AUTHOR_INVERTED_INDEX
        ARTICLE_INDEX = {}
        TAG_INVERTED_INDEX = {}
        AUTHOR_INVERTED_INDEX = {}

    def dump_index(self):
        dat = shelve.open(INDEX_DAT)
        dat["article_index"] = ARTICLE_INDEX
        dat["tag_inverted_index"] = TAG_INVERTED_INDEX
        dat["author_inverted_index"] = AUTHOR_INVERTED_INDEX
        dat.close()

    def create_index(self, filename):
        self._current_file_index = os.path.splitext(os.path.basename(filename))[0]
        self._index_tags(self.meta.get("tags", []), self._current_file_index)
        self._index_authors(self.meta.get("authors", []), self._current_file_index)

        title = self.meta.get("title", [""])[0]
        if title == "":
            title = os.path.splitext(os.path.basename(filename))[0]

        publish_dates = self.meta.get("publish_date", [])
        if len(publish_dates) == 0:
            publish_date = self._parse_time(os.path.getctime(filename), "%Y-%m-%d")
        else:
            publish_date = publish_dates[0]

        ARTICLE_INDEX[self._current_file_index] = {
            "filename": filename,
            "modify_time": self._parse_time(os.path.getmtime(filename)),
            "title": title,
            "summary": self.meta.get("summary", [u""])[0],
            "authors": self.meta.get("authors", [u"匿名"]),
            "publish_date": publish_date,
            "tags": self.meta.get("tags", [])
        }

    def _parse_time(self, timestamp, pattern="%Y-%m-%d %H:%M:%S"):
        return datetime.fromtimestamp(timestamp).strftime(pattern)

    def _index_tags(self, tags, fid):
        for tag in tags:
            if tag in TAG_INVERTED_INDEX:
                TAG_INVERTED_INDEX[tag].append(fid)
            else:
                TAG_INVERTED_INDEX[tag] = [fid]

    def _index_authors(self, authors, fid):
        for author in authors:
            if author in AUTHOR_INVERTED_INDEX:
                AUTHOR_INVERTED_INDEX[author].append(fid)
            else:
                AUTHOR_INVERTED_INDEX[author] = [fid]
