from dotenv import load_dotenv
import os

load_dotenv()

#Module name resolver
module_name = None
module_name_ab = None

#Mock Exam related
EXAM_DONE = False
LATEST_GRADE = None
LATEST_SCORE = None
NEW_SCORE = False

#API related
API_KEY = ""
API_KEY_URL = "https://aistudio.google.com/app/apikey"
API_KEY_INVALID = True