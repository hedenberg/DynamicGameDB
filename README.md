#DynamicGameDB
For more information please visit [DynamicGameDB](https://sites.google.com/site/dynamicgamedb/) 

## Testing
```
pip install -r requirements.txt 
python runserver.py
```
Now visit `127.0.0.1:5500` in your favorit browser.

### Backend - Platform
Three endpoints implemented for platform: 

`platform/add` - `POST` name="platform_name" - creates a platform with that name and returns json for that platform

`platforms` - `GET` return json for all platforms

`platform/<id>` - `GET` returns json for platform with that id

### Backend - Game
Three endpoints implemented for game: 

`game/add` - `POST` title="game_title" platform_id="platform_id" - creates a game for that platform with that name and returns json for that game

`games` - `GET` return json for all games

`game/<id>` - `GET` returns json for game with that id

### Frontend - API 
`docs/api` - `GET` shows current API from frontend to backend 

