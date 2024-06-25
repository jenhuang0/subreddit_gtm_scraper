"""
This is a auto get the movie's information based on the img folder of the GuessTheMovie subreddit.
Use the image name to ask chatGPT answer the movie publish year, region, main actor and actress. 

"""

import requests
import json
import os
import csv
from openai import OpenAI

# Load the OpenAI credentials from openai-client.json
with open("openai-client.json") as f:
    credentials = json.load(f)

client = OpenAI(
    api_key=credentials["api_key"],
    organization=credentials["organization"],
)


def extract_img_list():
    image_folder = "img"
    movies_list = os.listdir(image_folder)
    movies_list = [
        movie.replace(".jpg", "").replace("_", " ")
        for movie in movies_list
        if "Unnamed_Image" not in movie
    ]
    return movies_list


def get_details_from_movies_list(movies_list):
    data = []
    for movie in movies_list:
        prompt = f"""
        Using the movie name '{movie}', provide the following details without any other information:
        director:
        starring:
        country:
        language:
        release_year:
        running_time:
        production_company:
        If there's anything you don't know, leave it blank.
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Provide detailed movie information.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            details = response.choices[0].message.content.strip().split("\n")
            movie_details = [movie] + [
                detail.split(": ", 1)[1] if ": " in detail else "" for detail in details
            ]
            data.append(movie_details)
        except Exception as e:
            print(f"Error obtaining details for {movie}: {e}")
            continue

    return data


def save_to_csv(data):
    headers = [
        "Movie Name",
        "Director",
        "Starring",
        "Country",
        "Language",
        "Release Year",
        "Running Time",
        "Production Company",
    ]
    try:
        with open("movie_details.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for row in data:
                writer.writerow(row)
    except Exception as e:
        print(f"Error writing to CSV: {e}")


movies_list = extract_img_list()
movie_data = get_details_from_movies_list(movies_list)
save_to_csv(movie_data)
