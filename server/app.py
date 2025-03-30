#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>')
def show_article(id):
    # Increment page views
    session['page_views'] = session.get('page_views', 0) + 1

    # Check if page_views exceeded limit (3 views)
    if session['page_views'] > 3:
        # Update error message to match the test expectation
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Fetch the article by its ID
    article = db.session.get(Article, id)

    # If article doesn't exist, return a 404 message
    if article is None:
        return jsonify({'message': 'Article not found.'}), 404
    
    # Return the article data as JSON
    return jsonify(article.to_dict())

if __name__ == '__main__':
    app.run(port=5555)
