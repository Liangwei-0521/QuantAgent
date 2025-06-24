### QuantAgent

查看Gemini APY KEY 支持的模型序列

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

#### How to build a base agent

Agent记忆能力的实现
