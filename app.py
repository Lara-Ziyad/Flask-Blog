from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

# Function to load posts from the JSON file
def load_posts():
    with open('data.json', 'r') as file:
        posts = json.load(file)
    return posts

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)