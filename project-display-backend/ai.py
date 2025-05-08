from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
# 从配置文件中读取数据
API_KEY = os.getenv("API_KEY")

client = OpenAI(api_key=API_KEY, base_url="https://openkey.cloud/v1")

def explain(word):
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    stream=False,
    messages=[
      {"role": "user", "content": f"解释一下：{word}"}
    ]
  )

  return completion.choices[0].message

def summary(text):
  completion = client.chat.completions.create(
    model="gpt-4o-mini",
    stream=False,
    messages=[
      {"role": "user", "content": f"简要概括：{text}"}
    ]
  )

  return completion.choices[0].message