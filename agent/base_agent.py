import os 
import sys
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import asyncio
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import MessagesPlaceholder, ChatPromptTemplate
from tool.memory import get_by_session_id
from langchain_core.runnables import RunnableWithMessageHistory


prompt = ChatPromptTemplate(
    [
        ('system', 'You are a smart assistant.'),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human', '{input}')
    ]
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
        self.chat_agent = ChatGoogleGenerativeAI(
            model=os.getenv('GEMINI_MODEL_NAME'), 
            temperature=0.2,
            model_kwargs={"streaming": True},
        )
        self.chat_bot = prompt | self.chat_agent
        self.chat_workflow = RunnableWithMessageHistory(
            self.chat_bot,
            get_by_session_id,
            input_messages_key="input", 
            history_messages_key="chat_history"
        )

    async def aresponse(self, session_id, input):
        full_output = ""
        async for chunk in self.chat_workflow.astream(
            {'input': input},
            config={"configurable": {"session_id": session_id}}
        ):
            full_output += chunk.content
        print(full_output)

        return full_output
    

async def main():
    
    agent = base_agent()
    session_id = "user_1"
    print("欢迎使用智能Agent, 输入 'exit' 可退出。\n")

    while True:
        question = input("😊 User: ")
        if question.lower() == "exit":
            break
        print("🤖 Agent: ", end="", flush=True)
        await agent.aresponse(session_id=session_id, input=question)
   
    


if __name__ == '__main__':

   asyncio.run(main())




