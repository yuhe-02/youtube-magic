import yaml
from flask import Flask
from flask_injector import FlaskInjector
from injector import inject, singleton
from endpoints.sample_endpoint import sample_bp
from endpoints.youtube_endpoint import youtube_bp
from models.YoutubeModel import YoutubeModel
from controllers.YoutubeController import YoutubeController

# TODO create class
# TODO create type anotation
with open("config.yml", "r") as file:
    config: yaml = yaml.safe_load(file)
PORT: int = config['server']['port']

app = Flask(__name__)

def configure(binder):
    infile: str = "files/watch-history_min.json"
    out: str = "files/res.json"
    binder.bind(YoutubeModel, to=YoutubeModel(history_file_dir=infile, out_file_dir=out), scope=singleton)
    binder.bind(YoutubeController, to=YoutubeController, scope=singleton)
    
# flaskインスタンスにblueprintインスタンスを登録
app.register_blueprint(sample_bp, url_prefix = '/api')
app.register_blueprint(youtube_bp, url_prefix = '/youtube')

FlaskInjector(app=app, modules=[configure])
if __name__ == "__main__":
    app.run(port=PORT, debug=True)