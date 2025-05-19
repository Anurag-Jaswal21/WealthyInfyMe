landing_bp = Blueprint('landing_bp', __name__)

@landing_bp.route('/')
def index():
    topics = ['Mysore', 'India', 'World', 'Cricket']
    news_data = {topic: fetch_news_by_query(topic) for topic in topics}
    return render_template('index.html', news_data=news_data)




  return render_template("ForYou/index.html")



  from flask import render_template
from app.app_factory import fetch_news_by_query  # adjust import path

@protected_bp.route('/foryou')
def forYou():
    topics = ['Mysore', 'India', 'World', 'Cricket']
    news_data = {topic: fetch_news_by_query(topic) for topic in topics}
    return render_template("ForYou/index.html", news_data=news_data)
