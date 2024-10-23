import yaml
from flask import Flask
from flask_injector import FlaskInjector
from injector import inject, singleton
from endpoints.sample_endpoint import sample_bp
from endpoints.youtube_endpoint import youtube_bp
from models.YoutubeModel import YoutubeModel
from models.PromptGemini import PromptGemini
from controllers.YoutubeController import YoutubeController

# TODO create class
# TODO create type anotation
class ApplicationRunner:
    def __init__(self, infile: str, out: str, port: int, debug: bool = True):
        self.infile: str = infile
        self.out: str = out
        self.port: int = port
        self.debug: bool = debug

    def configure(self, binder):
        binder.bind(YoutubeModel, to=YoutubeModel(history_file_dir=self.infile, out_file_dir=self.out), scope=singleton)
        binder.bind(YoutubeController, to=YoutubeController, scope=singleton)
        binder.bind(PromptGemini, to=PromptGemini, scope=singleton)

    def run(self):
        app = Flask(__name__)
        app.register_blueprint(sample_bp, url_prefix='/api')
        app.register_blueprint(youtube_bp, url_prefix='/youtube')
        FlaskInjector(app=app, modules=[self.configure])
        app.run(port=self.port, debug=self.debug)

def load_config(filepath: str):
    with open(filepath, "r") as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    config = load_config("config.yml")
    port = config['server']['port']
    
    runner = ApplicationRunner(
        infile="files/raw/watch-history_min.json",
        out="files/treat/valid_videos/valid_videos.json",
        port=port
    )
    runner.run()