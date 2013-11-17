#DynamicGameDB
For more information please visit [DynamicGameDB](https://sites.google.com/site/dynamicgamedb/) 

## Testing
We now use gunicorn instead of flasks `app.run` with eventlet workers to allow the server to handle two calls at one time.
```
pip install -r requirements.txt 
gunicorn -w 2 --worker-class eventlet runserver:app
```
Now visit `127.0.0.1:8000` in your favorit browser.

### Backend - Platform
Three endpoints implemented for platform: 

`/api/platform/add` - `POST` name="platform_name" - creates a platform with that name and returns json for that platform

`/api/platforms` - `GET` return json for all platforms

`/api/platform/<id>` - `GET` returns json for platform with that id

### Backend - Game
Three endpoints implemented for game: 

`/api/game/add` - `POST` title="game_title" platform_id="platform_id" - creates a game for that platform with that name and returns json for that game

`/api/games` - `GET` return json for all games

`/api/game/<id>` - `GET` returns json for game with that id

### Frontend - API 
`/docs/api` - `GET` shows current API from frontend to backend 

`/games` - `GET` for now it just returns a string with info of all games

`/game/<id>` - `GET` for now it just returns a string with info of that game

