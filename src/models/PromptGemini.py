import pathlib
import textwrap
import google.generativeai as genai
import os
import time
import requests

from models.ThrowPrompt import PromptInterface

class PromptGemini(PromptInterface):
	def __init__(self):
		super().__init__()
		genai.configure(api_key=self.config["GEMINI_API_KEY"])
		model = genai.GenerativeModel('gemini-pro')
		self.chat = model.start_chat(history=[])
		self.summary = ""


	def split_text(self, text="", max_tokens=2000):
		return super().split_text(text, max_tokens)

	'''
		Args:
			log_file(str): the content of request
			out_path(str): the directory of output
			phase(int): phase flag
						1: represent when requesting summary
						2: represent when requesting question
						3: represent when requesting question but already defined summary(self.summary)
		Returns:
			str: the result of prompt.
		Raises:
			LinAlgException: If the matrix is not numerically invertible.
	'''
	def request(self, log_file, phase) -> str:
		chunks: list = []
		request_format: str = ""
		result: str = ""
		if phase == 1:
			chunks = self.split_text(text=log_file)
			request_format = self.summary_state
		elif phase == 2:
			chunks = self.split_text(text=log_file)
			request_format = self.question_state
		elif phase == 3:
			chunks = self.split_text(text=log_file)
			request_format = self.fruent_state
		else:
			chunks = self.split_text(text=self.summary)
			request_format = self.question_state

		for chunk in chunks:
			max_retries: int = 5
			retries: int = 0
			while retries < max_retries:
				try:
					response = self.chat.send_message(f'{request_format}:\n\n{chunk}')
					result += response.text + "\n"
					print(response._error)
					break
				except Exception as e:
					print(f"An error occurred: {e}")
					retries += 1
					wait_time = 2 ** (retries * 2)  # エクスポネンシャルバックオフ
					print(f"リトライ {retries}/{max_retries}: TooManyRequestsエラーが発生しました。再試行まで待機します...")
					time.sleep(wait_time)
			if (retries >= max_retries):
				raise ValueError("もうまじむり")
		self.summary = result
		return result

# if __name__ == "__main__":
#     model: PromptGemini = PromptGemini()
#     with open("../result/summary_no_spaces.txt", 'r', encoding='utf-8') as file:
#         content: str = file.read()
#     print(model.request(content, "res", 2))