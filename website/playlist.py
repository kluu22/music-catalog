"""
Store standard root for user page navigation
"""

from flask import Blueprint, render_template, request
from .models import Track, Score

# define blueprint for flask application
playlist = Blueprint('playlist', __name__)

@playlist.route('/create_playlist')
def home():
    # render our create_playlist.html in template
    return render_template("create_playlist.html")

@playlist.route('/create_playlist_top', methods=['GET'])
def create_playlist_top():
    top_num = request.args.get("top")
    tracks = Track.query.order_by(Track.score.desc()).limit(top_num)
    return render_template("create_playlist.html", tracks=tracks, selection=True)

@playlist.route('/create_playlist_bottom', methods=['GET'])
def create_playlist_bottom():
    bottom_num = request.args.get("bottom")
    tracks = Track.query.order_by(Track.score).limit(bottom_num)
    return render_template("create_playlist.html", tracks=tracks, selection=True)




