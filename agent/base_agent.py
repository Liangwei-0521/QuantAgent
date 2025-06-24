import os 
import sys 
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate


prompt = PromptTemplate(
    input_variables = [], 
    template='You are a stock trader'
)


# ✅ 加载配置文件
env_file = os.path.join(os.path.dirname(os.getcwd()), 'QuantAgent', '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)


os.environ["GOOGLE_API_KEY"] = os.getenv('GEMINI_API_KEY')


print(os.getenv('GEMINI_MODEL_NAME'))

# 🚩 实例化Agent
class base_agent:


    def __init__(self):

        self.LLM = ChatGoogleGenerativeAI(
            model = os.getenv('GEMINI_MODEL_NAME'), 
            temperature=0.2
            )
        

    def response(self, input):
        # invoke or stream 两种调用方式
        answer = self.LLM.stream(
            input=input
        )

        full_output = ""
        for chunk in answer:
            print(chunk.content, end="", flush=True)
            full_output  += chunk.content


        return full_output
    

if __name__ == '__main__':

    agent = base_agent()
    answer = agent.response('股票投资是好事吗')
    print(answer)
    print(type(answer))

        
    

