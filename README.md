# music-catalog
MedRhythms Demo Project: A Music Catalog

## Stacks
### Frontend
```
HTML
CSS
JAVASCRIPT
BOOTSTRAP
JINJA
```
### Backend
```
PYTHON
FLASK
```
### Database
```
SQLAlchemy
```

## Flask Application Structure
```
.
|──────test/
| |────__init__.py
| |────conftest.py
| |────functional/
| | |────__init__.py
| | |────test_tracks.py
|──────website/
| |────__init__.py
| |────catalog.py
| |────models.py
| |────playlist.py
| |────views.py
| |────static/
| | |────index.js
| |────templates/
| | |────base.html
| | |────catalog.html
| | |────create_playlist.html
| | |────home.html
| | |────ingest_data.html
|──────backend play-log.csv
|──────Backend track-metadata.json
|──────main.py
```

## Run Flask Application
```
Go to project directory and use the comman 'pip install -r requirements.txt' to install packages then 
find main.py and run main. From output in console, click the link routing to your localhost for the website link.
```

## Application Workflow

Use the nav bar to navigate through each page. 
Go to Catalog page then go to Ingest Track Data page to ingest track data. 
Go back to Catalog page to view the track records currently in the database.
Go back to Ingest Track Data page to ingest score data and a suitability score for each track 
will automatically be calculated and updated to the database. 
Go back to the Catalog page to view the overall score for each track.
From there, click sort (asc) or sort (desc) to sort the table based on score.
Then go to Create Playlist page to create playlist based on score rating. 

## Run PyTest
```
In music-catalog dir run: 'python3 -m pytest' in terminal
```

