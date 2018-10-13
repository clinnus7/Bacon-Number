# NO IMPORTS ALLOWED!

import json

filename = 'resources/names.json'
with open(filename, 'r') as f:
    names = json.load(f) # Dictionary with keys as actor names and values as actor IDs

filename = 'resources/movies.json'
with open(filename, 'r') as f:
    movies = json.load(f) # Dictionary with keys as actor names and values as actor IDs

def find_actor(actor_id):
    # Finds an actor's name based on actor_id
    for actor in names:
        if names[actor] == actor_id:
            return actor

def find_actor_id(actor):
    # Finds an actor's ID based on actor name
    return names[actor]

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    # Checks if two actors have worked together. Returns true if they have and false if they haven't
    for film in data:
        if actor_id_1 in film:
            if actor_id_2 in film:
                return True
    return False 

def get_actor_dic(data):
    # Makes a dictionary with the keys as all the actors in the data set and the values as lists of the actors the key has acted with 
    actor_dic = {}
    for film in data:
        if film[0] not in actor_dic:
            actor_dic[film[0]] = set([])
        if film[0] != film[1] and film[1] not in actor_dic[film[0]]:
            actor_dic[film[0]].add(film[1])
        
        if film[1] not in actor_dic:
            actor_dic[film[1]] = set([])
        if film[1] != film[0] and film[0] not in actor_dic[film[1]]:
            actor_dic[film[1]].add(film[0])

    return actor_dic

def get_actors_with_bacon_number(data, n):
    # Performs a breadth first search with starting location of 4724. Finds all actors connected with him, they become the next frontier, then find all the actors connected to those and so on.
    # Do this until bacon number is reached then add those actors to a separate list and return it
    actor_dic = get_actor_dic(data)
    visited = set([4724]) # Keeps track of all actors IDs visited
    frontier = [4724] # Keeps track of actors connected to the an actor that need to be checked
    bacon_number = 1
    actors_with_n = set([])

    while frontier:
        if bacon_number > n: # Ending condition where we return actors of a certain bacon number
            if len(actors_with_n) == 0:
                return {None}
            return actors_with_n

        next_frontier = []
        for actor in frontier: # Starts as 4724 then becomes a for loop of all the connections he has
            for coworker in actor_dic[actor]: 
                if coworker not in visited:
                    if bacon_number == n: # BACON NUMBER REACHED
                        actors_with_n.add(coworker)
                    visited.add(coworker) # Keeps track of which actors have been visited
                    next_frontier.append(coworker)

        if next_frontier == []:
            return set([])
        frontier = next_frontier # Frontier becomes the next group of actors, so on first pass it will become actors of bacon number 1
        bacon_number += 1

def get_bacon_path(data, actor_id):
    # Same concept as get_actors_with_bacon_number but also stores which actor connects to which through the parent dictionary
    actor_dic = get_actor_dic(data)
    visited = set([4724]) # Keeps track of all actors IDs visited
    frontier = [4724] # Keeps track of actors connected to the an actor that need to be checked
    parents = {4724: None} 
    path = []
    while frontier:
        next_frontier = []
        for actor in frontier:
            for coworker in actor_dic[actor]:
                if coworker not in visited:
                    visited.add(coworker)
                    next_frontier.append(coworker)
                    parents[coworker] = actor
                    if coworker == actor_id: # Once we find the actor we are looking for
                        while parents[actor_id] != None: # Goes through all the parents and adds them to a list in order until we get to 4724 which has a value of None
                            actor_id = parents[actor_id]
                            path = [actor_id] + path
                        return path + [coworker]
        if next_frontier == []:
            return None
        frontier = next_frontier 

    

def get_path(data, actor_id_1, actor_id_2):
    #Same as get_bacon_path except the starting point will be actor_id_1 instead of 4724
    actor_dic = get_actor_dic(data)
    visited = set([actor_id_1]) # Keeps track of all actors IDs visited
    frontier = [actor_id_1] # Keeps track of actors connected to the an actor that need to be checked
    parents = {actor_id_1: None} 
    path = []

    if (actor_id_1 not in actor_dic) or (actor_id_2 not in actor_dic): #If one or both of the actors isn't in the dataset return None
        return None

    while frontier:
        next_frontier = []
        for actor in frontier:
            for coworker in actor_dic[actor]:
                if coworker not in visited:
                    visited.add(coworker)
                    next_frontier.append(coworker)
                    parents[coworker] = actor
                    if coworker == actor_id_2:
                        while parents[actor_id_2] != None:
                            actor_id_2 = parents[actor_id_2]
                            path = [actor_id_2] + path
                        return path + [coworker]
        if next_frontier == []:
            return None 
        frontier = next_frontier

def get_movie_name(movie_id):
    # Returns the name of a movie based on movie ID
    for movie in movies:
        if movies[movie] == movie_id:
            return movie

def get_movie_path(data,actor_id_1,actor_id_2):
    # Uses the actor path to find the movies linking actors
    path = get_path(data,actor_id_1,actor_id_2)
    if path == []:
        return {}
    ind = 0
    actor_pairs = []
    while ind < len(path)-1: # Creates a list of lists with each inner list as a pair of actors that worked together. EX: [[1,2],[3,4]}
        actor_pairs.append([path[ind],path[ind+1]])
        ind += 1

    unordered_movies = {}
    for movie in data: # Goes through each movie in entire data set
        for pair in actor_pairs: 
            if pair[0] in movie and pair[1] in movie: # Checks to see if pair acted in each movie
                unordered_movies[movie[2]] = actor_pairs.index(pair) # If so the movie_id is added to a dictionary with value as the index of the actor pair
                actor_pairs[actor_pairs.index(pair)] = [None,None] # Then we replace the actor IDs for that pair with None so that actor pair is not used again

    number_movies = len(unordered_movies)
    movie_path = [0] * number_movies # Creates list filled with 0's so we can assign values based on index
    
    for movie in unordered_movies: # Assigns movie names to dictionary value, which is the index
        movie_path[unordered_movies[movie]] = get_movie_name(movie)

    return movie_path 





if __name__ == '__main__':
    # with open('resources/small.json') as f:
    #     smalldb = json.load(f)
    
    # filename = 'resources/tiny.json'
    # with open(filename, 'r') as f:
    #     tinydb = json.load(f)

    filename2 = 'resources/large.json'
    with open(filename2, 'r') as f:
        largedb = json.load(f)

    # print("start")
    a = get_actors_with_bacon_number(largedb,4)
    b = get_bacon_path(largedb,find_actor_id("Stephen Blackehart"))
    c = get_path(largedb,find_actor_id("Tim Matheson"),find_actor_id("Tatsuya Ishiguro"))

    # print(a)
    # final = []
    # for each in a:
    #     final.append(find_actor(each))
    # print(final)
    # print(find_actor_id("Tim Matheson"))
    # print(find_actor_id("Tatsuya Ishiguro"))




    
    # a = get_actors_with_bacon_number(largedb,3)
    # b = set([])
    # for each in a:
    #     b.add(find_actor(each))
    # print(b)



    
    # print(did_x_and_y_act_together(smalldb, find_actor_id("Stephen Blackehart"), find_actor_id("Kaj Nilsson")))
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
