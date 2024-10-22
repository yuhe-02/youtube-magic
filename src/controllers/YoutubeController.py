from flask import jsonify, Response
import json
from injector import inject
from models.YoutubeModel import YoutubeModel

# TODO add description
class YoutubeController:
	@inject
	def __init__(self, youtube_model: YoutubeModel):
		self.youtube_model = youtube_model

	def execute(self) -> list:
		video_list: list = self.youtube_model.extract_valid_video()
		self.youtube_model.save_results()
		response_data = json.dumps(video_list, ensure_ascii=False, indent=4).encode('utf-8')
		return Response(response=response_data, mimetype='application/json')