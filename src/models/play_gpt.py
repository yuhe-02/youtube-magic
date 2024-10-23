from openai import OpenAI
import openai
import os
import time

from models.ThrowPrompt import PromptInterface

class PromptGpt(PromptInterface):
	def __init__(self):
		super().__init__()
		SECRET_OPENAI_KEY: str = self.config["GPT_API_KEY"]
		self.model = OpenAI(
			api_key=SECRET_OPENAI_KEY,
		)
		self.summary = ""


	def split_text(self, text="", max_tokens=500):
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
				print(len(f'{request_format}\n\n{chunk}'))
				gpt_response: any = self.model.chat.completions.create(
					messages=[
						{	
							'role': 'user', 
							'content': f'{request_format}\n\n{chunk}'
						}
					],
					model='gpt-3.5-turbo',
				)
				result += gpt_response['choices'][0]['message']['content'] + "\n"
		except openai.RateLimitError:
			print("Rate limit exceeded, waiting to retry...")
			time.sleep(10)  # 10秒待機して再試行
		except Exception as e:
			print(f"An error occurred: {e}")
		self.summary = result
		return result

# if __name__ == "__main__":
#     model: PromptGpt = PromptGpt()
#     with open("../result/summary_no_spaces.txt", 'r', encoding='utf-8') as file:
#         content: str = file.read()
#     print(model.request(content, 2))