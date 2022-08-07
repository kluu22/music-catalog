from flask import url_for
from sqlalchemy import select, func

from website import create_app, db
from website.models import Track, Score


def test_create_track(app_db):
    """
    GIVEN a Flask application configured for testing
    WHEN make post request to '/ingest_track_data_manually' with track data
    THEN check that track entry with that uuid is inserted into the DB
    """
    response = app_db.post(url_for("catalog.ingest_track_data_manually"),
                                data={
                                    "uuid": "0Mickey0-0000-0000-0000-000Mickey000",
                                    "title": "Mickey Sings",
                                    "artist": "Mickey Mouse",
                                    "beat_map": "[22.2, 33.3, 44,4]",
                                    "bpm": 21.1
                                })

    assert response.status_code == 200
    count = db.session.execute(select(func.count(Track.id)).where(Track.uuid == "0Mickey0-0000-0000-0000-000Mickey000")).scalar_one()
    assert count == 1


def test_insert_duplicate_track_uuid(app_db):
    """
    GIVEN a Flask application configured for testing
    WHEN make post request to '/ingest_track_data_manually' with track data
    THEN check that track entry with existing uuid is NOT inserted into the DB and record count still is 1
    """
    response = app_db.post(url_for("catalog.ingest_track_data_manually"),
                                data={
                                    "uuid": "0Mickey0-0000-0000-0000-000Mickey000",
                                    "title": "Mickey Sings",
                                    "artist": "Mickey Mouse",
                                    "beat_map": "[22.2, 33.3, 44,4]",
                                    "bpm": 21.1
                                })
    count = db.session.execute(select(func.count(Track.id)).where(Track.uuid == "0Mickey0-0000-0000-0000-000Mickey000")).scalar_one()
    assert count == 1