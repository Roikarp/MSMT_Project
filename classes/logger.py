import logging

class logger:
	def __init__(self, logger_path):
		self.logger_obj = logging.getLogger(__name__)
		self.logger_obj.setLevel(logging.INFO)
		file_handler = logging.FileHandler(logger_path)
		formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
		file_handler.setFormatter(formatter)
		# Add the file handler to the logger
		self.logger_obj.addHandler(file_handler)

	def info(self, messege):
		# Log a message to the file
		self.logger_obj.info(messege)
