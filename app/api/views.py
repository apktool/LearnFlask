from flask import redirect, url_for, request, jsonify, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
from .helper import IndexData
from .generate import generate
from . import api
from ..decorators import admin_required
import os
import pdb

INPUT_CONTENT = './app/blog/MD'


@api.route('/file/upload', methods=['POST'])
@login_required
def upload_article():
    f = request.files['md_file']
    f_name = secure_filename(f.filename)
    path = os.path.join(os.getcwd(), INPUT_CONTENT, f_name)
    f.save(path)

    '''
    geninstance = generate()
    geninstance.load_all_md_files(INPUT_CONTENT)
    geninstance.gen_all_to_html()
    '''

    geninstance = generate()
    geninstance.load_md_file(f_name)
    geninstance.gen_to_html(f_name)
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
def generate_index():
    try:
        geninstance = generate()
        geninstance.load_all_md_files(INPUT_CONTENT)
        geninstance.gen_all_to_html()
        # geninstance.clean()
        geninstance.dump_index()
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
