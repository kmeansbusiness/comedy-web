## Comedy Web

An analysis of comedy actors and their most frequent collaborators, using IMDB data.

## Research Questions

### What are the most central communities within this network?
We tried a few out of the box clique / community clustering algorithms, but with no obvious insights. We need to find a way to filter out large cliques that are only connected by a single movie.

### Who is the most well connected actor?
Will Ferrell (see `get_most_connected_actor`)
TODO: see which movies connect him to other actors.

### What are some fun shortest path examples?
Think of random actor pairings and run shortest path on them.

## Running the code
Create and activate virtualenv:
```
python -m venv env
source env/bin/activate
```
Install dependencies:
```
pip install -r requirements.txt
```
