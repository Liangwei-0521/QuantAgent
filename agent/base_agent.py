import os 
import sys 
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI



# ✅ 加载配置文件
env_file = os.path.join(os.path.dirname(os.getcwd()), 'QuantAgent', '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)



class base_agent:


    def __init__(self):

        pass 


