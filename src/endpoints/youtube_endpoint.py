from flask import Blueprint
from injector import inject
from controllers.YoutubeController import YoutubeController

'''
	description: 
'''
# TODO create class
# TODO create type anotation
youtube_bp = Blueprint('youtube', __name__)

@youtube_bp.route('/', methods=['GET'])
@inject
def execute(youtube_controller: YoutubeController):
    return youtube_controller.execute()