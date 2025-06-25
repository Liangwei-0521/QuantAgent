### QuantAgent

#### 功能介绍

##### 1、查看Gemini APY KEY 支持的模型序列

```python
import os 
import google.generativeai as genai
from dotenv import load_dotenv


env_file = os.path.join(os.path.dirname(os.getcwd()), 'QuantAgent', '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)


os.environ["GOOGLE_API_KEY"] = os.getenv('GEMINI_API_KEY')


genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

models = genai.list_models()
for m in models:
    print(m.name)

```

##### 2、Agent记忆能力的实现

```python
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
```


3、MCP第三方服务
