from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, VideoUnavailable, TooManyRequests
import json
from time import sleep
from datetime import datetime
from tqdm import tqdm
import signal
import sys

class YoutubeModel:
	def __init__(self, history_file_dir: str = "", out_file_dir: str = ""):
		self.history_file_dir = history_file_dir
		self.available_videos: list = []
		self.out_file_dir = out_file_dir
		signal.signal(signal.SIGINT, self.signal_handler)

	def signal_handler(self, signum, frame):
		self.save_results()

	def get_json_file(self, dir: str = "") -> list:
		with open(dir, 'r', encoding='utf-8') as file:
			historys_json: list = json.load(file)
		return (historys_json)

	def save_results(self):
		print("結果を保存しています...")
		with open(self.out_file_dir, 'w', encoding="utf-8") as f:
			json.dump(self.available_videos, f, ensure_ascii=False, indent=4)
		# sys.exit(0)

	def extract_valid_video(self, his_file_dir: str = "") -> list:
		target_file: str = self.history_file_dir
		if (his_file_dir != ""):
			target_file = his_file_dir
		videos_json: list = self.get_json_file(target_file)
		for node in tqdm(videos_json):
			video_id: str = node["titleUrl"].replace("https://www.youtube.com/watch?v=", "")
			max_retries: int = 5
			retries: int = 0
			while retries < max_retries:
				try:
					transcript_list = YouTubeTranscriptApi.list_transcripts(video_id=video_id)
					self.available_videos.append(node)
					break
				except TooManyRequests as T:
					retries += 1
					print(f"リトライ {retries}/{max_retries}: TooManyRequestsエラーが発生しました。再試行します...")
					sleep(8)
				except Exception as e:
					print(f"他のエラーが発生しました: {e}")
					break
			if retries >= max_retries:
				raise ValueError("もう少し時間を置いてから再実行してください。")
		return self.available_videos
	def create_full_output():
		return None

# if __name__ == "__main__":
# 	timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
# 	history_file_dir: str = "../Takeout_3/YouTube/history/watch-history.json"
# 	out_file_dir: str = f"../config/valid_history/history_{timestamp}.json"
# 	mag: YoutubeManager = YoutubeManager(history_file_dir=history_file_dir, out_file_dir=out_file_dir)
# 	res: list = YoutubeManager.extract_valid_video(mag)
# 	with open(out_file_dir, 'w', encoding='utf-8') as file:
# 		json.dump(res, file, ensure_ascii=False, indent=4)