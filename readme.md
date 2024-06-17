# Movie Guessing Insights Project

## Overview

This project leverages data from the "GuessTheMovie" subreddit to provide insightful visualizations about various movies. The primary goal is to crawl image URLs and movie names from the subreddit posts, enrich the data using the OpenAI API, and visualize the results using Tableau.

## Features

- **Data Extraction**: Uses Reddit API to fetch data from the "GuessTheMovie" subreddit.
- **Data Enrichment**: Utilizes OpenAI API to gather detailed information about each movie.
- **Data Visualization**: Employs Tableau to create insightful visualizations and dashboards.
  
## Data Pipeline

1. **Reddit API**: Extracts images and corresponding movie names from the "GuessTheMovie" subreddit.
2. **Data Processing**:
   - Image URLs and movie names are collected.
   - OpenAI API is used to obtain detailed movie information, including:
     - Movie Name
     - Director
     - Starring
     - Country
     - Language
     - Release Year
     - Running Time
     - Production Company
3. **Data Storage**: Compiles the data into a CSV file.
4. **Data Visualization**: Imports the CSV file into Tableau for creating visual insights.

## Technologies Used

- **Reddit API**: For fetching data from the "GuessTheMovie" subreddit.
- **OpenAI API**: For enriching the data with detailed movie information.
- **Python**: For scripting and automation.
- **Tableau**: For data visualization.


## Prerequisites

- Python 3.7 or higher
- Tableau Public Desktop
- Reddit API credentials
- OpenAI API credentials

## Result
[Result](https://public.tableau.com/app/profile/jen.huang7878/viz/Moviesinspect/Dashboard2)