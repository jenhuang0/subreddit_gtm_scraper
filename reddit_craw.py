import praw
import requests
import os
import re
import json


# create a Reddit instance with reddit_credential.json
with open("reddit_credential.json") as f:
    credentials = json.load(f)
    reddit = praw.Reddit(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        user_agent=credentials["user_agent"],
        username=credentials["username"],
        password=credentials["password"],
    )
# reddit = praw.Reddit(
#     client_id="kCmpLPzl8985E-mA7gECpA",
#     client_secret="jIsrDAo3d4YfpBFtQuk8SEB-hSwTWA",
#     user_agent="WordCount",
#     username="melmujer",
#     password="JoelChang123!",
# )

# define the folder to save the images
image_folder = "img"
os.makedirs(image_folder, exist_ok=True)

# counter for unnamed images
unnamed_image_counter = 1
# get the subreddit
subreddit = reddit.subreddit("GuessTheMovie")

# iterate through the subreddit
for submission in subreddit.hot(limit=50):
    # check if the URL is an image
    if submission.url.endswith((".jpg", ".png", ".jpeg")):
        print("Title: ", submission.title)
        print("URL: ", submission.url)

        # attempt to fetch the first comment
        submission.comments.replace_more(
            limit=0
        )  # This line ensure that all MoreComments objects are removed
        if submission.comments.list():
            # if subission title has "[EASY]" in it or the first comment author is "GTMBot", then the second comment is the answer
            if (
                "[EASY]" in submission.title
                or submission.comments.list()[0].author == "GTMBot"
            ):
                comment = submission.comments.list()[1].body
            else:
                comment = submission.comments.list()[0].body

            print("First Valid Comment: ", comment)

            # extract text within quotes if present and more than 30 characters
            match = re.search(r'"([^"]+)"', comment)
            if match and len(match.group(1)) > 30:
                quoted_text = match.group(1)
                safe_filename = re.sub(r'[\\/*?:"<>|]', "", quoted_text).replace(
                    " ", "_"
                )
            elif len(comment) < 30:
                safe_filename = re.sub(r'[\\/*?:"<>|]', "", comment).replace(" ", "_")
            else:
                safe_filename = f"Unnamed_Image_{unnamed_image_counter}"
                unnamed_image_counter += 1
        else:
            safe_filename = f"Unnamed_Image_{unnamed_image_counter}"
            unnamed_image_counter += 1

        # sanitize the filename
        if not safe_filename.strip():
            safe_filename = f"Unnamed_Image_{unnamed_image_counter}"
            unnamed_image_counter += 1

        # download the image
        response = requests.get(submission.url)
        if response.status_code == 200:
            file_path = os.path.join(image_folder, f"{safe_filename}.jpg")

            # save the image
            with open(file_path, "wb") as f:
                f.write(response.content)
            print("Image saved at: ", file_path)
        else:
            print("Failed to download image")
