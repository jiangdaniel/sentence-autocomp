from flask import Flask
from flask import request
from sentences import Lexicon

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World!"

# Data in post request should have parameter 'text'
@app.route('/train', methods=['POST'])
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
