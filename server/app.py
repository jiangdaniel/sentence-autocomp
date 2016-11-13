from flask import Flask
from flask import request
from sentences import Lexicon

# Imports for the @crossdomain decorator
from datetime import timedelta
from flask import Flask, make_response, request, current_app
from functools import update_wrapper

# Provides the @crossdomain from http://flask.pocoo.org/snippets/56/
def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

# Data in post request should have parameter 'text'
@app.route('/train', methods=['POST', 'OPTION'])
@crossdomain(origin='*')
def train():
    if request.method == 'POST':
        lexicon = Lexicon()
        lexicon.add_text(request.form['text'])
        result = ""
        for sentence in lexicon.sentences:
            result += sentence.data + "\n"
        return result

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/js', methods=['GET', 'POST'])
def js():
    if request.method == 'POST':
        return request.form['text']
    else:
        return "JS request URI"

if __name__ == "__main__":
    app.run()
