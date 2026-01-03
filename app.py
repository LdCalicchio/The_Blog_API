import os
from urllib.parse import quote_plus
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD'))}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.JSON, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now)
    updatedAt = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "content" : self.content,
            "category" : self.category,
            "tags" : self.tags,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }

with app.app_context():
    db.create_all()

# Defining routes
# Home
@app.route("/")
def home():
    return "Hello, this is the Blog API"

# GET
@app.get('/posts')
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts])

@app.get('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)
    if post:
        return jsonify(post.to_dict())
    else:
        return jsonify({"error":"Not Found"}), 404
    
# @app.get('/posts/<str:post_id>')
# def get_post(post_id):
#     post = Post.query.get(post_id)
#     if post:
#         return jsonify(post.to_dict())
#     else:
#         return jsonify({"error":"Not Found"}), 404

# UPDATED POST
@app.post('/posts')
def create_post():
    data = request.get_json()

    if isinstance(data, list):
        posts_data = data
    else:
        posts_data = [data]

    created_posts = []

    for item in posts_data:
        new_post = Post(
            title=item["title"],
            content=item["content"],
            category=item["category"],
            tags=item["tags"]
        )
        db.session.add(new_post)
        created_posts.append(new_post)

    db.session.commit()

    results = [post.to_dict() for post in created_posts]

    if isinstance(data, list):
        return jsonify(results), 201
    else:
        return jsonify(results[0]), 201

# PUT -> Update
@app.put('/posts/<int:post_id>')
def update_post(post_id):
    data = request.get_json()

    post = Post.query.get(post_id)
    if post:
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        post.category = data.get("category", post.category)
        post.tags = data.get("tags", post.tags)
        post.updatedAt = datetime.now()

        db.session.commit()

        return jsonify(post.to_dict()), 200
    else:
        return jsonify({"404":"Not Found"}), 404

# DELETE
@app.delete('/posts/<int:post_id>')
def delete_post(post_id):
    post = Post.query.get(post_id)

    if post:
        db.session.delete(post)
        db.session.commit()

        return jsonify({"204": "No content"}), 204
    else:
        return jsonify({"404":"Not Found"}), 404
    
if __name__ == "__main__":
    app.run(debug=True)