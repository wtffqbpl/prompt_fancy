#! coding: utf-8

import os
import requests
from dotenv import load_dotenv, find_dotenv
from utils.tools import get_model_name, get_completion, split_think_answer


def translate_city_name(city_name: str) -> str:
    """Translate a city name to English using a language model."""
    model_name = get_model_name()

    prompt = f"""
    The specified city name is '{city_name}', \
    If the city name is not in English, \
    then translate the city name '{city_name}' to English.
    
    **ONLY RETURN THE ENGLISH NAME OF THE CITY, NO OTHER INFORMATION.**
    """

    # Get the completion from the model
    response, _ = get_completion(prompt, model=model_name)
    return response


def get_weather(location: str) -> str:
    """Get the weather information."""
    _ = load_dotenv(find_dotenv())
    api_key = os.environ["OPEN_WEATHER_API_KEY"]
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": translate_city_name(location),
        "appid": api_key,
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn"  # 中文描述
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['cod'] != 200:
            return f"Get weather failed: {data.get('message', 'Unknown error')}"

        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        desc = data['weather'][0]['description']

        result = (
            f"城市: {city}, 国家: {country}\n"
            f"温度: {temp}°C, 体感温度: {feels_like}°C\n"
            f"湿度: {humidity}%, 风速: {wind_speed} m/s\n"
            f"天气状况: {desc}"
        )
        return result

    except  requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Cannot fetch weather data at the moment."
    except Exception as e:
        return f" An unknown error: {e}"


def search_internet(query: str, max_results: int = 3) -> str:
    """Search the internet for a query and return the top results."""
    _ = load_dotenv(find_dotenv())
    serper_api_key = os.environ["GOOGLE_SERPER_SEARCH_API_KEY"]
    search_url = "https://google.serper.dev/search"

    payload = {
        "q": query,
    }

    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(search_url, json=payload, headers=headers)
        result = response.json()

        # Acquire the top max_results results
        snippets = []
        for item in result.get('organic', [])[:max_results]:
            title = item.get('title', 'No title')
            snippet = item.get('snippet', 'No snippet')
            link = item.get('link', 'No link')
            snippets.append(f"{title}\n{snippet}\n{link}\n")

        return "\n".join(snippets)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Cannot perform search at the moment."
    except Exception as e:
        return f" An unknown error: {e}"


if __name__ == '__main__':
    # print(get_weather("珠海"))
    print(search_internet("Python programming language"))


