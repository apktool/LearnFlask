from flask import redirect, url_for, request
from werkzeug.utils import secure_filename
from . import api
from .generate import generate
import os
import pdb

INPUT_CONTENT = './app/blog/MD'

@api.route('/file/upload', methods=['POST'])
def upload_article():
    f = request.files['md_file']
    f_name = secure_filename(f.filename)
    path = os.path.join(os.getcwd(), INPUT_CONTENT , f_name)
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
