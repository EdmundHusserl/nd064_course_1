import sqlite3
import logging
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    url_for,
    redirect,
    flash,
)
import uuid
from werkzeug.exceptions import abort
from middleware import AppLogger


logger = AppLogger(name="app", level=10)


@logger.increment("db_connection_count")
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection


@logger.increment("post_count")
def create_post(title: str, content: str):
    connection = get_db_connection()
    connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                       (title, content))
    connection.commit()
    connection.close()


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute(
        'SELECT * FROM posts WHERE id = ?',
        (post_id,)
    ).fetchone()
    connection.close()
    return post


def get_post_count() -> int:
    connection = get_db_connection()
    post_count = connection.execute(
        "SELECT * FROM posts"
    ).fetchall()
    connection.close()
    return len(post_count)


logger.set_post_count(count=get_post_count())


def create_flask_instance() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = uuid.uuid4().hex
    app.logger = logger.logger
    return app


app = create_flask_instance()


@app.route("/")
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


@app.route("/<int:post_id>")
def post(post_id):
    post = get_post(post_id)

    if post is None:
        app.logger.info("A non-existing article is accessed.")
        return render_template('404.html'), 404
    else:
        app.logger.info(f"An existing article is retrieved: {post['title']}")
        return render_template('post.html', post=post)


@app.route("/about")
def about():
    app.logger.info("The \"About Us\" page has been retrieved")
    return render_template('about.html')


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!', category="error")

        else:
            create_post(title, content)
            app.logger.info(f"A new article is created: {title}")
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route("/healthz")
def health_probe() -> dict:
    return jsonify({"result": "OK - healthy"}), 200


@app.route("/metrics")
def metrics() -> dict:
    return jsonify({
        "db_connection_count": logger.db_connection_count,
        "post_count": logger.post_count
    }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3111', debug=True)
