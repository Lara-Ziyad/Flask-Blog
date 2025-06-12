from flask import Flask
import json

app = Flask(__name__)

# Function to load posts from the JSON file
def load_posts():
    with open('data.json', 'r') as file:
        posts = json.load(file)
    return posts


# Helper: fetch post by ID
def fetch_post_by_id(post_id):
    blog_posts = load_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

from flask import request, redirect, url_for, render_template


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load current posts
        blog_posts = load_posts()

        # Generate new ID → one higher than current max ID
        new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1

        # Create new post dictionary
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Add new post to list
        blog_posts.append(new_post)

        # Save back to JSON
        with open('data.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect to home page
        return redirect(url_for('index'))

    # If GET → show form
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load posts
    blog_posts = load_posts()

    # Remove post with matching ID
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save updated list back to JSON
    with open('data.json', 'w') as file:
        json.dump(blog_posts, file, indent=4)

    # Redirect to home page
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch all posts
    blog_posts = load_posts()

    # Find the post to update
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # Get updated data from form
        updated_author = request.form.get('author')
        updated_title = request.form.get('title')
        updated_content = request.form.get('content')

        # Update the post fields
        for p in blog_posts:
            if p['id'] == post_id:
                p['author'] = updated_author
                p['title'] = updated_title
                p['content'] = updated_content
                break

        # Save updated posts back to JSON
        with open('data.json', 'w') as file:
            json.dump(blog_posts, file, indent=4)

        # Redirect to home
        return redirect(url_for('index'))

    # GET → show form pre-filled with post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)