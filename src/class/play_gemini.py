import pathlib
import textwrap
import google.generativeai as genai
import os
import time

from throw_prompt import PromptInterface

class PromptGemini(PromptInterface):
	def __init__(self):
		super().__init__()
		genai.configure(api_key="")
		self.model = genai.GenerativeModel('gemini-pro')
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
	def request(self, log_file, phase):
		chunks: list = []
		request_format: str = ""
		result: str = ""
		if phase == 1:
			chunks = self.split_text(text=log_file)
			request_format = self.summary_state
		elif phase == 2:
			chunks = self.split_text(text=log_file)
			request_format = self.question_state
		else:
			chunks = self.split_text(text=self.summary)
			request_format = self.question_state

		try:
			for chunk in chunks:
				response = self.model.generate_content(f'{request_format}:\n\n{chunk}')
				result += response.text + "\n"
				time.sleep(8)
		except Exception as e:
			print(f"An error occurred: {e}")
		self.summary = result
		return result

# if __name__ == "__main__":
#     model: PromptGemini = PromptGemini()
#     with open("../result/summary_no_spaces.txt", 'r', encoding='utf-8') as file:
#         content: str = file.read()
#     print(model.request(content, "res", 2))