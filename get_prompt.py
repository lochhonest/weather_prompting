import openai
import os
from get_weather import get_weather



def get_prompt():
    openai.api_key = OPENAI_API_KEY
    GPT_MODEL = "gpt-3.5-turbo-1106"

    def row_to_string(df, row_index):
        row = df.iloc[row_index]
        return ', '.join([f'{col}: {row[col]}' for col in df.columns])
    
    df_input = get_weather()
    weather_summaries = []
    for i in range(len(df_input)):
        weather_sum = row_to_string(df_input, i)
        weather_summaries.append(weather_sum)


    def get_weather_prompt(weather_summaries):
        prompts= []
        for weather_summary in weather_summaries:
            try:
                messages=[
                        {"role": "system", "content": "You are designed to craft effective prompts for images. You like using descriptive words over numbers."},
                        {"role": "user", "content": f"Read the following weather data and craft an image prompt, which within 50 tokens, effectively captures the atmosphere: {weather_summary}"}]
                response = openai.chat.completions.create(
                    model=GPT_MODEL,
                    messages=messages,
                    seed=42,
                    max_tokens=50,
                    temperature=0.7,
                )
                prompts.append(response.choices[0].message.content)
            except Exception as e:
                print("An error occurred:", e)
        return prompts
    prompts = get_weather_prompt(weather_summaries)
    return prompts


