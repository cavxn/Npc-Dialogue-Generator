import google.generativeai as genai

genai.configure(api_key="AIzaSyCSuzugJNBX05RO3PKd4bNXd0LmrFu9qbM")

model = genai.GenerativeModel("gemini-pro")

response = model.generate_content("Write a short story about a time-traveling turtle.")

print(response.text)
