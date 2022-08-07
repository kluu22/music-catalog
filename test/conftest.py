import pytest
from sqlalchemy import delete

from website import create_app, db
from website.models import Track, Score

@pytest.fixture(scope="session")
def flask_app():
    app = create_app()

    client = app.test_client()

    context = app.test_request_context()
    context.push()

    yield client

    context.pop()

@pytest.fixture(scope="session")
def app_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()

@pytest.fixture
def app_data(app_db):
    track = Track()
    track.uuid = "9bTEST50-5166-TEST-80c0-bTESTUUID90d"
    track.title = "Some Test Title Single"
    track.artist = "Test Artist"
    track.beat_map = "[0.36, 1.02, 1.67, 2.32, 2.97, 3.63, 4.28, 4.93, 5.59, 6.25, 6.9, 7.55, 8.19, 8.85, 9.49, 10.14, 10.78, 11.43, 12.08, 12.72, 13.36, 14.0, 14.64, 15.27, 15.91, 16.56, 17.21, 17.84, 18.48, 19.12, 19.76, 20.4, 21.03, 21.68, 22.33, 22.97, 23.61, 24.25, 24.9, 25.53, 26.17, 26.82, 27.45, 28.09, 28.73, 29.38, 30.02, 30.66, 31.29, 31.94, 32.59, 33.23, 33.87, 34.52, 35.17, 35.8, 36.43, 37.08, 37.72, 38.36, 38.99, 39.64, 40.28, 40.91, 41.54, 42.19, 42.83, 43.47, 44.1, 44.76, 45.41, 46.04, 46.67, 47.32, 47.96, 48.6, 49.23, 49.88, 50.51, 51.15, 51.79, 52.44, 53.08, 53.73, 54.36, 55.01, 55.65, 56.29, 56.92, 57.57, 58.21, 58.85, 59.49, 60.13, 60.77, 61.41, 62.05, 62.7, 63.34, 63.97, 64.61, 65.25, 65.89, 66.53, 67.17, 67.81, 68.45, 69.08, 69.72, 70.36, 70.99, 71.63, 72.27, 72.91, 73.56, 74.2, 74.83, 75.47, 76.11, 76.75, 77.38, 78.02, 78.66, 79.29, 79.93, 80.56, 81.19, 81.83, 82.46, 83.1, 83.74, 84.38, 85.02, 85.67, 86.32, 86.95, 87.59, 88.24, 88.88, 89.52, 90.15, 90.8, 91.44, 92.08, 92.72, 93.37, 94.02, 94.66, 95.3, 95.96, 96.6, 97.23, 97.87, 98.52, 99.16, 99.8, 100.44, 101.09, 101.74, 102.37, 103.01, 103.65, 104.3, 104.94, 105.58, 106.22, 106.87, 107.5, 108.14, 108.78, 109.42, 110.07, 110.7, 111.34, 111.99, 112.62, 113.26, 113.9, 114.55, 115.19, 115.83, 116.48, 117.12, 117.76, 118.4, 119.06, 119.71, 120.36, 121.0, 121.66, 122.31, 122.94, 123.57, 124.22, 124.87, 125.53, 126.17, 126.82, 127.46, 128.11, 128.75, 129.4, 130.05, 130.7, 131.35, 132.0, 132.63, 133.27, 133.91, 134.57, 135.22, 135.87, 136.5, 137.14, 137.79, 138.44, 139.08, 139.73, 140.37, 141.01, 141.66, 142.31, 142.95, 143.6, 144.24, 144.88, 145.53, 146.17, 146.82, 147.46, 148.11, 148.75, 149.38, 150.03, 150.68, 151.32, 151.96, 152.6, 153.23]"
    track.bpm = "23.5"
    db.session.add(track)

    score = Score()
    score.entrainment_pct = "0.516"
    score.end_reason = "SKIP"
    score.uuid = "9bTEST50-5166-TEST-80c0-bTESTUUID90d"
    db.session.add(score)

    db.session.commit()

    yield app_db

    db.session.execute(delete(Track))
    db.session.execute(delete(Score))
    db.session.commit()