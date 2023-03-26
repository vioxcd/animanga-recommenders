# Anime and Manga Recommendation System

This repository shows a simple deployment of an anime and manga recommendation system model and users' favorites association rules. Deployment is done using [FastAPI](https://fastapi.tiangolo.com/). It only uses a sample of data (4 records) for demonstration purposes.

The recommendation model is taken from my Bachelor thesis experiment result and [demo](./notebooks/Demo_CDRS.ipynb). The demo is tidy and doesn't include the scraper, cleaning routine, and other tests (skip to the bottom of the notebook to see the recommendation in action!)

The experiments are published as paper and it can be accessed [here](https://ieeexplore.ieee.org/abstract/document/9946560)

The association rules is a project I've done a while back that is related to this one, and I find it interesting so I include it here. The implementation is simple, mostly uses what's already given by Spark's [FP-Growth algorithm](https://spark.apache.org/docs/latest/ml-frequent-pattern-mining.html). The implementation can be found [here](./notebooks/Spark_Association_Rules.ipynb)

## Installation

Use the `build-docker.sh` script to build the image

```bash
# execute the script to build the image
chmod +x ./build-docker.sh
./build-docker.sh

# running the image
docker run -d --name CONTAINER_NAME -p 8000:80 animanga-recommenders-fastapi:latest

# either access your browser and go to http://localhost:8000/recs/USER_ID (integer between 0-3) or... (don't forget that last "/" ...)
curl -X GET http://localhost:8000/recs/USER_ID/
```

## Usage

There's 3 endpoint:

- `/recs/USER_ID` — used for anime and manga recommendation (matrix factorization)
- `/favs_assoc/USER_ID` — used for anime and manga recommendation (association rules)
- `/search_rules/SECTION/?query=QUERY` — sections is a value of either `[anime, manga, characters, people]` and query is the name/title of the section. this endpoint returns the rule for entered query

For trying out, visit `http://localhost:8000/docs`

## Some Pics

### The API

![Neat docs from FastAPI](./images/3-api-docs.png)

![It's outputting the same thing as with the Demo CDRS](./images/2-api-result.png)

![Get recommendation for users via association rules](./images/6-get-recs.png)

![Try to search for rules. Penguindrum! It's a great anime](./images/7-search-for-penguindrum.png)

### Building the Image and Notes about Docker

![It's running smoothly!](./images/1-building-docker-image.png)

![I took some notes regarding Docker](./images/4-docker-notes.png)

### Association Rule Recs for Me & Training

![Recommendations for me by the association rule model](./images/5-recs-for-me.png)

![It's using n=15 and taking so long! (almost 30 miutes) ended up using n=20 which takes seconds...](./images/8-training-association-rules.png)

![How favorites looks like in MAL](./images/9-favorites.png)
