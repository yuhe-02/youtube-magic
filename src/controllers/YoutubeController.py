from flask import jsonify, Response
import json
from injector import inject
from models.YoutubeModel import YoutubeModel
from models.PromptGemini import PromptGemini

# TODO add description
class YoutubeController:
	@inject
	def __init__(self, youtube_model: YoutubeModel, gemini_model: PromptGemini):
		self.youtube_model = youtube_model
		self.gemini_model = gemini_model

	def execute(self) -> list:
		video_list: list = self.youtube_model.extract_valid_video()
		self.youtube_model.save_results()
		response_data = json.dumps(video_list, ensure_ascii=False, indent=4).encode('utf-8')
		return Response(response=response_data, mimetype='application/json')

	def execute2(self) -> list:
		res: str = self.youtube_model.create_full_output()
		response_data = json.dumps(res, ensure_ascii=False, indent=4).encode('utf-8')
		return Response(response=response_data, mimetype='application/json')

	def execute3(self) -> list:
		with open("./files/treat/subtitles/raw/qnNhZ8sHWjg-20241023223534.json", "r", encoding="utf-8") as file:
			content = json.load(file)
		res: str = self.gemini_model.request(content, 3)
		response_data = json.dumps(res, ensure_ascii=False, indent=4).encode('utf-8')
		return Response(response=response_data, mimetype='application/json')