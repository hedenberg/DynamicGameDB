from dynamicgamedb import app
import flask

@app.route('/', methods=['GET'])
def home():
    print "Katten"
    return "Hello there"
