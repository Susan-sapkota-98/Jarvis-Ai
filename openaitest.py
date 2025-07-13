import openai
from config import apikey

openai.api_key = apikey

def test_openai():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Write an email to my boss for resignation?"}]
        )
        print("AI Response:\n")
        print(response["choices"][0]["message"]["content"])
    except Exception as e:
        print("Error from OpenAI:", e)

if __name__ == "__main__":
    test_openai()
