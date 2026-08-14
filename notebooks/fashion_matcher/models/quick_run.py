from openai import OpenAI
import ollama

model_name = 'qwen2.5vl:7b'

client = OpenAI(
    base_url="http://localhost:11434/v1",  # change to port 8000 if using vLLM
    api_key="ollama",  # dummy key required by client but ignored locally
)

response = client.chat.completions.create(
    model=model_name,  # replace with your local model tag (e.g., qwen2.5, qwen3-8b)
    messages=[{"role": "user", "content": "Hello, Qwen!"}],
)

print(response.choices[0].message.content)



# Replace 'qwen2.5' with your specific local Qwen model tag (e.g., 'qwen3:8b')


# 1. Non-streaming response
response = ollama.chat(
    model=model_name,
    messages=[{'role': 'user', 
               # 'content': 'Explain the difference between a list and a tuple in Python.'
               'content': 'describe this image: D:\\code\\pythondemo\\notebooks\\fashion_matcher\\kate_perry.jpg'
               }]
)
print("--- Standard Response ---")
print(response['message']['content'])

# 2. Streaming response (displays text as it is generated)
print("\n--- Streaming Response ---")
stream = ollama.chat(
    model=model_name,
    messages=[{'role': 'user', 'content': 'Write a 3-sentence poem about space.'}],
    stream=True
)

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
print()