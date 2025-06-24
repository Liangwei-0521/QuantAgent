import os 
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableWithMessageHistory



# ✅ 加载配置文件
env_file = os.path.join(os.path.dirname(os.getcwd()), 'QuantAgent', '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)


os.environ["GOOGLE_API_KEY"] = os.getenv('GEMINI_API_KEY')


# 创建提示模版
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),  # 🧠 加入历史上下文！
    ("human", "{input}")
])


# 创建 LLM 对象
llm = ChatGoogleGenerativeAI(model=os.getenv('GEMINI_MODEL_NAME'))



store = {}


from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    '''In memory implementation of chat message history'''

    messages: list[BaseMessage] = Field(default_factory=list)
    def add_messages(self, messages: list[BaseMessage]) -> None:
        "Add a list of messages to the store"
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []

def get_by_session_id(session_id:str) -> BaseChatMessageHistory:

    if session_id not in store:
        store[session_id] = InMemoryHistory()

    return store[session_id]


# 用于运行的 chain：Expression Language
chat_chain = prompt | llm



from langchain_core.runnables import RunnableWithMessageHistory


chat_bot = RunnableWithMessageHistory(
    chat_chain,
    get_by_session_id, 
    input_messages_key="input", 
    history_messages_key="chat_history"

)


session_id = "user_1"

response = chat_bot.invoke(
    {"input": "我叫小明"}, 
    config={"configurable": {"session_id": session_id}}
)
print(response.content)

response = chat_bot.invoke(
    {"input": "我是谁？"}, 
    config={"configurable": {"session_id": session_id}}
)
print(response.content)
