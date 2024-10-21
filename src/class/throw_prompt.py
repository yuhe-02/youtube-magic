import pathlib
import textwrap
import google.generativeai as genai
import os
import time
from openai import OpenAI
import openai

class PromptInterface:
    def __init__(self):
        self.question_state = self.get_text_from_txt("../config/prompt/request_question.txt")
        self.summary_state = self.get_text_from_txt("../config/prompt/request_summary.txt")

    def get_text_from_txt(self, dir: str):
        with open(dir, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

    def split_text(self, text="", max_tokens=2000) -> list:
        whole_text_len: int = len(text) - 1
        index: int = 0
        chunk: list = []
        while (index < whole_text_len):
            if whole_text_len - index < max_tokens:
                chunk.append(text[index : whole_text_len + 1])
                break
            chunk.append(text[index : index + max_tokens])
            index += max_tokens
        return (chunk)

    def request_summary(self, log_file):
        raise NotImplementedError("このメソッドはサブクラスで実装する必要があります。")
    
    def request_question(self, summary_file):
        raise NotImplementedError("このメソッドはサブクラスで実装する必要があります。")