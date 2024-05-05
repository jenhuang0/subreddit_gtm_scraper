import praw
import requests
import os
import re
import json


def create_reddit_instance():
    """
    Create a Reddit instance using the credentials from 'reddit_credential.json'.

    Returns:
        praw.Reddit: The Reddit instance.
    """
    with open("reddit_credential.json") as f:
        credentials = json.load(f)
        reddit = praw.Reddit(
            client_id=credentials["client_id"],
            client_secret=credentials["client_secret"],
            user_agent=credentials["user_agent"],
            username=credentials["username"],
            password=credentials["password"],
        )
    return reddit


def create_image_folder():
    """
    Create image folder name "img"

    Returns:
        image_folder
    """
    image_folder = "img"
    os.makedirs(image_folder, exist_ok=True)
    return image_folder


def get_submission_comments(submission):
    submission.comments.replace_more(limit=0)
    return submission.comments.list()


def get_first_valid_comment(comments, submission):
    if comments:
        if "[EASY]" in submission.title or comments[0].author == "GMTBot":
            comment = comments[1].body
        else:
            comment = comments[0].body
        return comment
    return None


def extract_quoted_text(comment):
    match = re.search(r'"([^"]+)"', comment)
    if match and len(match.group(1)) > 30:
        return match.group(1)
    return None


def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename).replace(" ", "_")


def process_subreddit(subreddit_name, limit=50):
    reddit = create_reddit_instance()
    subreddit = reddit.subreddit(subreddit_name)
    image_folder = create_image_folder()
    unnamed_image_counter = 1

    for submission in subreddit.hot(limit=limit):
        if submission.url.endswith((".jpg", ".png", ".jpeg")):
            print("Title: ", subreddit.title)
            print("URL: ", subreddit.url)

            comments = get_submission_comments(submission)
            comment = get_first_valid_comment(comments, submission)

            if comment:
                quoted_text = extract_quoted_text(comment)
                if quoted_text:
                    safe_filename = sanitize_filename(quoted_text)
                elif len(comment) < 30:
                    safe_filename = sanitize_filename(comment)
                else:
                    sefa_filename = f"Unnamed_Image_{unnamed_image_counter}"
                    unnamed_image_counter += 1
            else:
                safe_filename = f"Unnamed_Image_{unnamed_image_counter}"
                unnamed_image_counter += 1

            # sanitize the filename:
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


def main():
    subreddit_name = "GuessTheMovie"
    limit = 50
    process_subreddit(subreddit_name, limit)


if __name__ == "__main__":
    main()
