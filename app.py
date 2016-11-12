from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

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
