from flask import jsonify

class SampleController:
	@staticmethod
	def example():
		return jsonify(message="This is the response from the /example endpoint.")