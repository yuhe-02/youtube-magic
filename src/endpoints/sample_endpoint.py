from flask import Blueprint
from controllers.SampleController import SampleController

'''
	description: 
'''
sample_bp = Blueprint('sample', __name__)

@sample_bp.route('/', methods=['GET'])
def example():
    return SampleController.example()