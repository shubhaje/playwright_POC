from google import genai
client = genai.Client(api_key="AIzaSyABfa8pNMvflYjWnP1MmEh2YEuM67aAyxc")

for m in client.models.list():
    print(m.name)