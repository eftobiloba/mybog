from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class blogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Blog post {str(self.id)}"

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/posts', methods=['GET'])
def list_posts():
    post_list = blogPost.query.order_by(desc(blogPost.date_posted)).all()
    return render_template('posts.html', posts= post_list[:2], s_posts= post_list[3:], t_posts= post_list[2])

@app.route('/posts/addpost', methods=['GET', 'POST'])
def add_posts():
    if request.method == "POST":
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = blogPost(title = post_title, content = post_content, author = post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')

    else:
        return render_template('addPost.html')

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = blogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = blogPost.query.get_or_404(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

@app.route('/posts/read/<int:id>', methods=['GET'])
def read(id):
    post = blogPost.query.get_or_404(id)
    return render_template('read.html', post=post)

@app.route('/home/<string:name>')
def HelloWorld(name):
    return f"Hello {name}!"

@app.route('/onlyget', methods=['GET'])
def get_req():
    return "You can only get this webpage"

if __name__ == "__main__":
    app.run(debug= True)