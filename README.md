# Personalized Book Recommender System
Leveraging the Amazon Books Reviews dataset to create a system that recommends books based on users' reading history and preferences.

## Very Important!
If you want to locally deploy the API, you have to copy the [Amazon Books Reviews](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews) dataset into `data/raw` (a folder that must be created manually the first time), as the docker containers will expect these files to exist:
- `data/raw/books_data.csv`
- `data/raw/Books_rating.csv`

You can then run `docker compose build` and `docker compose run`

## Project Overview
In today's digital age, with the vast plethora of books available online, finding the next best book to read can be overwhelming. This project aims to develop a recommendation system that curates a list of books tailored to users' tastes, utilizing both Collaborative Filtering and Content-Based Filtering methodologies.

## Dataset
Source: [Amazon Books Reviews](https://www.kaggle.com/datasets/mohamedbakhet/amazon-books-reviews)

### Description:
The dataset contains user reviews for various books available on Amazon. It includes product metadata and provides a comprehensive view of user interactions with books, offering insights into user preferences and behavior.

## Objectives
1. **Data Cleaning & Preprocessing:** Handling missing values, removing duplicates, and preprocessing text data.
1. **Exploratory Data Analysis (EDA):** Gain insights into the distribution of ratings, popular books, active reviewers, etc.
1. **Collaborative Filtering Implementation:** Build a model that recommends books based on user-user or item-item similarity.
1. **Content-Based Filtering Implementation:** Use the review text and metadata to recommend books similar to a given book or based on user's past preferences.
1. **Hybrid Model:** Combine both collaborative and content-based filtering for enhanced recommendations.
1. **Evaluation:** Assess the accuracy and efficiency of the recommendation models using appropriate metrics.

## Technical Stack
- Language: Python
- Libraries: pandas, scikit-learn, numpy, tensorflow, nltk
