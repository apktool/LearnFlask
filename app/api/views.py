from flask import redirect, url_for, request, jsonify, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from .helper import IndexData
from .generate import generate_html, generate_index
from .render import render
from ..models import Post
from . import api
from ..decorators import admin_required
import os
import pdb

INPUT_CONTENT = './app/blog/MD'


@api.route('/file/upload', methods=['POST'])
@login_required
def upload_article():
    f = request.files['md_file']
    name = secure_filename(f.filename)

    name = os.path.join(os.getcwd(), INPUT_CONTENT, name)
    f.save(name)

    f_name = str(Post.query.count() + 1) + '.' + name.split('.')[-1]
    f_name = os.path.join(os.getcwd(), INPUT_CONTENT, f_name)

    os.rename(name, f_name)

    '''
    geninstance = generate_html()
    geninstance.load_all_md_files(INPUT_CONTENT)
    geninstance.gen_all_to_html()
    '''

    renderinstance = render(f_name)
    meta = renderinstance.render_to_html()

    genhtmlinstance = generate_html(meta)
    genhtmlinstance.load_md_file(f_name)
    genhtmlinstance.gen_to_html(f_name)

    # genindexinstance = generate_index(meta)
    # pdb.set_trace()
    # IndexData.reload_index_data()
    return redirect(url_for("main.index"))


@api.route('/gen/posts')
def get_all_post_index():
    return jsonify(IndexData.get_index_data().get("article_index"))


@api.route('/gen/inv_tag')
def get_tag_index():
    return jsonify(IndexData.get_index_data().get("tag_inverted_index"))


@api.route('/gen/inv_author')
def get_author_index():
    return jsonify(IndexData.get_index_data().get("author_inverted_index"))


@api.route('/gen/reload')
def reload_index():
    try:
        IndexData.reload_index_data()
        return jsonify({"msg": "ok"})
    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({"msg": "failed"})


@api.route('/gen/generate')
def generate_to_index():
    flag = True
    try:
        '''
        genhtmlinstance = generate_html()
        genhtmlinstance.load_all_md_files(INPUT_CONTENT)
        genhtmlinstance.gen_all_to_html()
        # geninstance.clean()
        '''
        
        for root, _, f_names in os.walk(INPUT_CONTENT):
            for f_name in f_names:
                f_name = os.path.join(INPUT_CONTENT, f_name)

                renderinstance = render(f_name)
                meta = renderinstance.render_to_html()

                genindexinstance = generate_index(meta)
                if flag is True:
                    flag = False
                    genindexinstance.drop_index()
                genindexinstance.create_index(f_name)
                genindexinstance.dump_index()

                IndexData.reload_index_data()

        return jsonify({"msg": "ok"})
    except Exception as e:
        current_app.logger.exception(e)
        return jsonify({"msg": "failed"})


@api.route('/gen/tag/<tag>')
def get_article_by_tag(tag):
    aids = IndexData.get_index_data().get("tag_inverted_index").get(tag)
    posts = {i: IndexData.get_index_data().get("article_index")[i] for i in aids}
    return jsonify(posts)
