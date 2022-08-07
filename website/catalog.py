from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Track, Score
from . import db
import json
import csv

# define blueprint for flask application
catalog = Blueprint('catalog', __name__)

@catalog.route('/catalog', methods=['GET', 'POST'])
def home():
    """
    :return: '/catalog' page
    Query for all track records and display it in a table
    Show score column if score column is populated for each track else do not show
    """
    tracks = Track.query.all()
    scores = list(Track.query.values(Track.score))
    score_available = True
    if all(score[0] == None for score in scores):
        score_available = False

    return render_template("catalog.html", tracks = tracks, score_available = score_available)

@catalog.route('/sort_score_inc', methods=['GET', 'POST'])
def sort_score_inc():
    """
    :return: '/catalog' page
    Query for all track records in ascending order by score and display it in a table
    """
    tracks = Track.query.order_by(Track.score)
    return render_template("catalog.html", tracks=tracks, score_available=True)

@catalog.route('/sort_score_desc', methods=['GET', 'POST'])
def sort_score_desc():
    """
    :return: '/catalog' page
    Query for all track records in decreasing order by score and display it in a table
    """
    tracks = Track.query.order_by(Track.score.desc())
    return render_template("catalog.html", tracks = tracks, score_available = True)

@catalog.route('/ingest_track_data', methods=['GET', 'POST'])
def ingest_track_data():
    """
    :return: 'ingest_data' page
    """
    return render_template("ingest_data.html")

@catalog.route('/ingest_track_data_by_filename', methods=['GET', 'POST'])
def ingest_track_data_by_filename():
    """
    :return: '/ingest_data' page
    Upon getting a POST request, load in track data from the specified JSON file from user
    """
    if request.method == 'POST':
        filename = request.form.get('filename')
        if filename:
            load_database(filename)
            flash("Track data from JSON file ingested successfully! Please go to Catalog page to view tack.", category='success')
        else:
            flash("Missing filename. Please select filename and try again.", category='error')

    return render_template("ingest_data.html")

@catalog.route('/ingest_track_data_manually', methods=['GET', 'POST'])
def ingest_track_data_manually():
    """
    :return:  '/ingest_data' page
    Upon getting a POST request, load in track data from the specified fields from user
    """
    uuid = request.form.get('uuid')
    title = request.form.get('title')
    artist = request.form.get('artist')
    beat_map = request.form.get('beat_map')
    bpm = request.form.get('bpm')
    # print("{} {} {} {} {}".format(uuid, title, artist, beat_map, bpm))

    if request.method == 'POST':
        if uuid and title and artist and artist and beat_map and bpm:
            new_track = Track(
                uuid=uuid,
                title=title,
                artist=artist,
                beat_map=beat_map,
                bpm=bpm
            )
            try:
                db.session.add(new_track)
                db.session.commit()
            except Exception as e:
                print("Failed to import track. {}".format(e))
                flash("Track data ingested NOT successfully! Duplicate UUID.", category='error')
                db.session.rollback()
                return render_template("ingest_data.html")
            flash("Track data ingested successfully! Please go to Catalog page to view.", category='success')
        else:
            flash("Missing field/fields. Cannot ingest into DB. Please check!", category='error')

    return render_template("ingest_data.html")

@catalog.route('/calculate_suitability_score', methods=['GET', 'POST'])
def calculate_suitability_score():
    """
    :return: '/ingest_data' page
    Upon getting a POST request, load in score track data from the specified CSV file from user
    """
    if request.method == 'POST':
        filename = request.form.get('score_filename')
        if filename:
            data = read_csv(filename)
            load_database_score(data)
            flash(f"Score track data from CSV file ingested successfully! Please go to Catalog page to view score.",
                  category='success')
        else:
            flash("Missing filename. Please select filename and try again.", category="error")
    return render_template("ingest_data.html")

def load_database(filename):
    """
    :param filename: str
    :return: none
    Iterate through the JSON and parse each data and insert each track record into DB
    List of beat map is cleaned to have exactly two decimal points percision
    """
    tracks = read_json(filename)
    # print(tracks)
    # ONLY: uuid, track title, artist, beat_map, bpm
    for i in range(len(tracks)):
        beat_map = clean_decimal_percision(tracks[i]['beat_map'])
        new_track = Track(
            uuid=str(tracks[i]['uuid']),
            title=str(tracks[i]['title']),
            artist=str(tracks[i]['artist']),
            beat_map= beat_map,
            bpm=float(tracks[i]['bpm'])
        )
        try:
            db.session.add(new_track)
            db.session.commit()

        except Exception as e:
            print("Failed to import track. {}".format(e))
            pass

def load_database_score(data):
    """
    :param data: csv data
    :return: none
    Iterate through each data in CSV and insert into Score table
    Use a dictionary data structure to keep track of overall score
    for each unique key uuid when iterating through each record in CSV
    At the end, iterate through each overall score in dictionary and update score column of Track table
    """
    from collections import defaultdict
    tracks_score_map = defaultdict(int)

    for row in data:
        uuid = row[0]
        entrainment_pct = float(row[1])
        end_reason = row[2]
        # print(f'{uuid} {entrainment_pct} {end_reason}')
        # insert record into Score table
        new_score = Score(
            uuid=uuid,
            entrainment_pct=entrainment_pct,
            end_reason=end_reason,
        )
        try:
            db.session.add(new_score)
            db.session.commit()

        except Exception as e:
            flash(f"Fail to import score track record. {e}", category='error')
            pass

        score = calculate_score(entrainment_pct, end_reason)
        tracks_score_map[uuid] = tracks_score_map[uuid] + score

    for uuid, score in tracks_score_map.items():
        # print(f"{uuid}, {score}")
        Track.query. \
            filter(Track.uuid == uuid). \
            update({'score': score})
        db.session.commit()


def calculate_score(entrainment_pct, end_reason):
    """
    :param entrainment_pct: float
    :param end_reason: str
    :return: int

    Specify logic of scoring based on the following rules:
    Score +2:
    - `entrainment_pct` > 0.7
    Score +1:
    - `entrainment_pct` in range 0.5 - 0.7
    - `end_reason` == `NATURAL_END`
    Score -1:
    - `entrainment_pct` in range 0.3 - 0.5
    - `end_reason` == `USER_SKIP`
    Score -2:
    - `entrainment_pct` < 0.3
    """
    score = 0
    if entrainment_pct >= 0.7:
        score = 2
    elif 0.5 <= entrainment_pct < 0.7 and end_reason == "NATURAL_END":
        score = 1
    elif 0.3 <= entrainment_pct < 0.5 and end_reason == "SKIP":
        score = -1
    elif entrainment_pct < 0.3:
        score = -2
    else:
        # No score is given since it doesn't fall under any rule
        # print(f"No score given. Entrainment_pct: {entrainment_pct} | end_reason: {end_reason}")
        pass
    return score

def clean_decimal_percision(beat_map):
    """
    :param beat_map: list
    :return: string representation of a list
    Iterate through each beat in beat_map and convert each float to two decimal points precision
    """
    new_beat_map = []
    for bm in beat_map:
        # convert each float to two decimal points precision
        bm = "{:.2f}".format(bm)
        new_beat_map.append(bm)

    # turn into string representation of a list bc column type is string in DB
    new_beat_map_str = ", ".join(new_beat_map)
    return "[" + new_beat_map_str + "]"

def read_json(filename="Backend track-metadata.json"):
    """
    :param filename: str
    :return: obj
    A helper function to read JSON file
    """
    with open(filename, "r") as json_file:
        data = json_file.read()
        obj = json.loads(data)
        return obj

def read_csv(filename="backend play-log.csv"):
    """
    :param filename: str
    :return: list
    A helper function to read CSV file
    """
    with open(filename, "r") as csv_file:
        data = csv.reader(csv_file, delimiter=",", quotechar='"')
        next(data, None)  # skip the headers
        data_read = [row for row in data]
        return data_read




