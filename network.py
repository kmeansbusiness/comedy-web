# boilerplate
import pandas as pd
import itertools
from collections import defaultdict
import json
import operator

# network stuff
import networkx as nx
# from pyvis.network import Network


def create_collab_dict(movie, collab_dict={}):
    """
    Takes in a movie dataframe with a row per actor and outputs a dictionary with a key representing a pair

    {
      ('Mark Wahlberg', 'Will Ferrell'): {
          'counts': 3,
          'movies':['The Other Guys', 'Daddy's Home', 'Daddy's Home 2']
          }
    }

    """
    pair_list = itertools.combinations(movie['actor_name'], 2)
    for pair in pair_list:
        collab_dict.setdefault(pair, {'weight': 0, 'movie_list': []})
        collab_dict[pair]['weight'] += 1
        collab_dict[pair]['movie_list'].append(movie['primaryTitle'].iloc[0])

    return collab_dict


def create_edges(df_main, movie_list):
    """
    Takes in main dataset, list of movies, and builds the edge dict
    """
    counter = 0
    edge_dict = {}

    print("Constructing edge list...")

    for movie in movie_list:
        movie_record = df_main.query("primaryTitle == @movie")
        edge_dict = create_collab_dict(movie_record, edge_dict)

        counter += 1
        if counter % 1000 == 0:
            print(f'Parsed {counter} movies')

        if counter == len(movie_list):
            print(f'Finished parsing {len(movie_list)} movies')

    return edge_dict


def create_network_graph(data_path):
    print(f'Loading data from {data_path}')
    df = pd.read_csv(data_path)

    # create actor df
    df_actor = df['primaryName'].value_counts().reset_index()
    df_actor.columns = ['actor_name', 'num_movies']

    # only look at actors who are in more than 5 movies
    df_actor_subset = df_actor[df_actor['num_movies'] > 5]

    # use this subset to filter our movie data
    df_movie_subset = df.merge(df_actor_subset, how='inner', left_on='primaryName', right_on='actor_name')
    df_movie_name = df_movie_subset['primaryTitle'].unique()

    # create the graph
    G = nx.Graph()
    G.add_nodes_from(df_actor_subset['actor_name'])
    edges = create_edges(df_movie_subset, df_movie_name)
    edge_list = [(a1, a2, attr) for (a1, a2), attr in edges.items()]
    G.add_edges_from(edge_list)
    return G


def get_most_connected_actor(G):
    centrality = nx.degree_centrality(G)
    top_pairs = sorted(centrality.items(), key=operator.itemgetter(1), reverse=True)

    for name, pct_nodes in top_pairs[:5]:
        print(name, pct_nodes)


def get_cliques(G):
    cliques = []
    for clique in nx.find_cliques(G):
        if len(clique) > 2:
            cliques.append((clique, len(clique)))

    import pdb; pdb.set_trace()

    for c, c_size in sorted(cliques, key=operator.itemgetter(1), reverse=True)[:10]:
        print(c, c_size)


if __name__ == "__main__":
    G = create_network_graph('data/comedies_actors.csv')
    top_pairs = sorted(G.edges.data('weight'), key=lambda r: r[2], reverse=True)[:3]
    print(f"Top Actor Pairs: {top_pairs}")

    # get_most_connected_actor(G)
    get_cliques(G)


    import pdb; pdb.set_trace()
