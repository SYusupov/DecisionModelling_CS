import math
import pandas as pd
import random
import numpy as np
import pandas as pd

def get_data(file):
    """
    Obtains a critiques dictionary from the data csv file
    """
    df = pd.read_excel(file)
    critiques = df.set_index('name').transpose().to_dict(orient='dict')
    movie_list = list(df.columns[1:])
    filtered_critiques = {person: {movie: value for movie, value in values.items() if value != 0.0 and not np.isnan(value)} for person, values in critiques.items()}
    return movie_list, filtered_critiques

def check_missing_data_percentage(movies, critiques):
    """
    Checks for missing data percentage in the critiques' evaluation matrix
    """
    total_cells = len(critiques) * len(movies)
    missing_cells = 0

    for person in critiques:
        for movie in movies:
            if movie not in critiques[person]:
                missing_cells += 1

    missing_percentage = round((missing_cells / total_cells) * 100, 2)

    # print(f'Total cells in the matrix: {total_cells}, while missing cells in the matrix: {missing_cells}.')
    # print(f'Thus, missing cells percentage for the matrix is: {missing_percentage}%.')

    if 30 <= missing_percentage <= 50:
        # print(f'Thus, missing cells percentage condition for the given matrix satisfies.\n')
        return True

    # print(f'So, missing cells percentage condition for the given matrix is not satisfied.\n')
    return False

def check_chosen_critique(name, movies, critiques):
    """
    Checks for chosen critique, to see if hasn't seen atleast half of the movies
    """
    n_movies = len(movies)
    count = 0

    person = critiques[name]

    for movie in movies:
        if movie not in person.keys():
            count += 1

    unseen_percentage = round((count / n_movies) * 100, 2)

    # print(f'Total movies: {n_movies}, while {name} has watched: {n_movies - count}.')
    # print(f'Thus, percentage of unseen movies for the {name} is: {unseen_percentage}%.')

    if unseen_percentage >= 50:
        # print(f'Thus, unseen movies percentage condition satisifies for {name} and the given matrix.\n')
        return True

    # print(f'So, unseen movies percentage condition is not satisified for {name} and the given matrix.\n')
    return False

def sim_distanceManhattan(person1, person2):
    """
    Measures Manhattan distance between different persons' choices
    """
    manhattan_dist = 0
    for movie, rating in person1.items():
        if movie in person2.keys():
            manhattan_dist += abs(person1[movie] - person2[movie])
    return manhattan_dist

def sim_distanceEuclidienne(person1, person2):
    """
    Measures Euclidienne distance between different persons' choices
    """
    euclidienne_dist = 0
    for movie, rating in person1.items():
        if movie in person2.keys():
            euclidienne_dist += (person1[movie] - person2[movie]) ** 2
    return math.sqrt(euclidienne_dist)

def sim_distanceMinkowski(person1, person2):
    """
    Measures Minkowski distance between different persons' choices
    """
    p = 3
    minkowski_dist = 0
    for movie, rating in person1.items():
        if movie in person2.keys():
            minkowski_dist += abs(person1[movie] - person2[movie]) ** p
    return math.pow(minkowski_dist, (1/p))

def sim_distancePearson(person1, person2):
    """
    Measures the Pearson similarity distance between different persons' choices
    """
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in person1:
        if key in person2:
            n += 1
            x = person1[key]
            y = person2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += x ** 2
            sum_y2 += y ** 2

    # Handling no common movies situation
    if n == 0:
        return 0 

    numerator = sum_xy - (sum_x * sum_y) / n
    denominator = math.sqrt((sum_x2 - (sum_x ** 2) / n) * (sum_y2 - (sum_y ** 2) / n))
    
    if denominator == 0:
        return 0
    else:
        return numerator / denominator

def sim_distanceCosine(person1, person2):
    """
    Measures the Cosine similarity distance between different persons' choices
    """
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0
    for key in person1:
        if key in person2:
            n += 1
            x = person1[key]
            y = person2[key]
            sum_xy += x * y
            sum_x2 += x ** 2
            sum_y2 += y ** 2
    denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)
    if denominator == 0:
        return 0
    else:
        return (sum_xy) / denominator

def computeNearestNeighbor(nouveauCritique, Critiques):
    distances = []
    for critique in Critiques:
        if critique != nouveauCritique:
            distance = sim_distanceManhattan(Critiques[critique], Critiques[nouveauCritique])
            distances.append((distance, critique))
    distances.sort()
    return distances

def recommendNearestNeighbor(nouveauCritique, Critiques):
    """
    Recommends nearest neighbors of nouveauCritique using Manhattan distance
    """
    recommended_list = []
    sorted_critique = computeNearestNeighbor(nouveauCritique, Critiques)
    nearestNeighbor = sorted_critique[0][1]
    for movie, rating in Critiques[nearestNeighbor].items():
        if movie not in Critiques[nouveauCritique]:
            recommended_list.append((movie, rating))
    return recommended_list

def Bestrecommend(nouveauCritique, Critiques, movie_list, similarity_function):
    """
    Recommends the best movie using different similarity functions
    """
    total = 0.0
    s = 0.0
    max_s_dash = 0
    movieRecommended = ""

    # Leave only movies that aren't seen by noveauCritique
    nouveauMovie = []
    for movie in movie_list:
        if movie not in Critiques[nouveauCritique]:
            nouveauMovie.append(movie)

    for movie in nouveauMovie:
        critique_list = []
        
        # Generate critique list having this new movie rated
        for critique, rating in Critiques.items():
            if movie in rating.keys():
                critique_list.append(critique)

        if critique_list:
            # Calculate total(nouveauMovie) and s(nouveauMovie)
            for critique in critique_list:
                nouveauMovieRating = Critiques[critique][movie]

                if similarity_function == "manhattan":
                    distanceOfCritique = sim_distanceManhattan(Critiques[nouveauCritique], Critiques[critique])
                    s += (1 / (1 + distanceOfCritique))
                    total += (nouveauMovieRating / (1 + distanceOfCritique))
                
                elif similarity_function == "euclidean":
                    distanceOfCritique = sim_distanceEuclidienne(Critiques[nouveauCritique], Critiques[critique])
                    s += (1 / (1 + distanceOfCritique))
                    total += (nouveauMovieRating / (1 + distanceOfCritique))

                elif similarity_function == "minkowski":
                    distanceOfCritique = sim_distanceMinkowski(Critiques[nouveauCritique], Critiques[critique])
                    s += (1 / (1 + distanceOfCritique))
                    total += (nouveauMovieRating / (1 + distanceOfCritique))
                
                elif similarity_function == "pearson":
                    distanceOfCritique = sim_distancePearson(Critiques[nouveauCritique], Critiques[critique])
                    s += (2 + distanceOfCritique)
                    total += (nouveauMovieRating * (2 + distanceOfCritique))
                
                elif similarity_function == "cosine":
                    distanceOfCritique = sim_distanceCosine(Critiques[nouveauCritique], Critiques[critique])
                    s += (2 + distanceOfCritique)
                    total += (nouveauMovieRating * (2 + distanceOfCritique))

                # print(similarity_function, 'distanceOfCritique', distanceOfCritique)
            s_dash = total / s
            # print('s_dash, movie: ', movie, s_dash)

            if s_dash > max_s_dash:
                max_s_dash = s_dash
                movieRecommended = movie

    return movieRecommended

def generate_ratings(n_critics=10, n_movies=15, perc_missing=0.4):
    """For questions 4 and 5
    Generating ratings with the speicifed number of critics, number of movies
    percentage of missing movies in ratings for all critics
    max rating = 5, min rating = 1"""

    critiques = {}

    movie_idxs = list(range(n_movies))
    movies = ["M"+str(x) for x in movie_idxs]

    # generate ratings for all movies and for all critics
    for critic_idx in range(n_critics):
        movies_ratings = {}
        for movie in movies:
            movies_ratings[movie] = random.randint(1,5)
        
        critiques["C"+str(critic_idx)] = movies_ratings
    
    # leave only (1-perc_missing) for ratings
    for critic in critiques:
        for movie in dict(critiques[critic]):
            choice = random.uniform(0, 1)
            if choice <= perc_missing:
                (critiques[critic]).pop(movie)

    return movies, critiques

print('----------------------------------------------------')
print('Example 1:------------------------------------------')
print('----------------------------------------------------')

# movie_list1 = ["Lady", "Snakes", "Luck", "Superman", "Dupree", "Night"]
# critiques1 = {"Lisa Rose": {'Lady': 2.5, 'Snakes': 3.5, 'Luck': 3.0, 'Superman': 3.5, 'Dupree': 2.5, 'Night': 3.0},
#               "Gene Seymour": {'Lady': 3.0, 'Snakes': 3.5, 'Luck': 1.5, 'Superman': 5.0, 'Dupree': 3.5,
#                                'Night': 3.0},
#               "Michael Phillips": {'Lady': 2.5, 'Snakes': 3.0, 'Superman': 3.5, 'Night': 4.0},
#               "Claudia Puig": {'Snakes': 3.5, 'Luck': 3.0, 'Superman': 4.0, 'Dupree': 2.5, 'Night': 4.5},
#               "Mick Lasalle": {'Lady': 3.0, 'Snakes': 4.0, 'Luck': 2.0, 'Superman': 3.0, 'Dupree': 2.0,
#                                'Night': 3.0},
#               "Jack Matthews": {'Lady': 3.0, 'Snakes': 4.0, 'Superman': 5.0, 'Dupree': 3.5, 'Night': 3.0},
#               "Toby": {'Snakes': 4.5, 'Superman': 4.0, 'Dupree': 1.0},
#               "Anne": {'Lady': 1.5, 'Luck': 4.0, 'Dupree': 2.0}
#               }

file1 = 'data1.xlsx'
movie_list1, critiques1 = get_data(file1)

# testing
print("LisaRose")
print(computeNearestNeighbor("Lisa Rose", critiques1))
print(recommendNearestNeighbor("Lisa Rose", critiques1))
print("Toby")
print(computeNearestNeighbor("Toby", critiques1))
print(recommendNearestNeighbor("Toby", critiques1))
print("Eucleadian between Lisa and Gene: ", sim_distanceEuclidienne(critiques1["Lisa Rose"], critiques1["Gene Seymour"]))

print("Movie recommended for Anne with Manhattan similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "manhattan")) + "\n")
print("Movie recommended for Anne with Euclidean similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "euclidean")) + "\n")
print("Movie recommended for Anne with Minkowski similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "minkowski")) + "\n")
print("Movie recommended for Anne with Pearson similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "pearson")) + "\n")
print("Movie recommended for Anne with Cosine similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "cosine")) + "\n")


print('----------------------------------------------------')
print('Example 2:------------------------------------------')
print('----------------------------------------------------')

# movie_list2 = ["Blues Traveler", "Broken Bells", "Deadmau5", "Norah Jones", "Phoenix", "Slightly Stoopid",
#                "The Strokes", "Vampire Weekend"]
# critiques2 = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0,
#                            "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
#               "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0,
#                        "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
#               "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0,
#                        "Phoenix": 5.0, "Slightly Stoopid": 1.0},
#               "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0,
#                       "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
#               "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0,
#                          "Vampire Weekend": 1.0},
#               "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0,
#                          "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
#               "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0,
#                       "Slightly Stoopid": 4.0, "The Strokes": 5.0},
#               "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5,
#                            "The Strokes": 3.0}
#               }

file2 = 'data2.xlsx'
movie_list2, critiques2 = get_data(file2)

print('\nFor Veronica:---------------------------------------')
print("Movie recommended for Veronica with Manhattan similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "manhattan")) + "\n")
print("Movie recommended for Veronica with Euclidean similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "euclidean")) + "\n")
print("Movie recommended for Veronica with Minkowski similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "minkowski")) + "\n")
print("Movie recommended for Veronica with Pearson similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "pearson")) + "\n")
print("Movie recommended for Veronica with Cosine similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "cosine")) + "\n")

print('\nFor Hailey:----------------------------------------')
print("Movie recommended for Hailey with Manhattan similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "manhattan")) + "\n")
print("Movie recommended for Hailey with Euclidean similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "euclidean")) + "\n")
print("Movie recommended for Hailey with Minkowski similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "minkowski")) + "\n")
print("Movie recommended for Hailey with Pearson similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "pearson")) + "\n")
print("Movie recommended for Hailey with Cosine similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "cosine")) + "\n")

print('Question4:-----------------------------------------------')
file3 = 'q4_data.xlsx'
movie_list3, critiques3 = get_data(file3)
# print(movie_list3, critiques3)
check_missing_data_percentage(movie_list3, critiques3)
check_chosen_critique('C9', movie_list3, critiques3)

print('Critic chosen for recommendation: C9.')
print("Movie recommended for C9 with Manhattan similarity distance: " + str(
    Bestrecommend("C9", critiques3, movie_list3, "manhattan")) + "\n")
print("Movie recommended for C9 with Euclidean similarity distance: " + str(
    Bestrecommend("C9", critiques3, movie_list3, "euclidean")) + "\n")
print("Movie recommended for C9 with Minkowski similarity distance: " + str(
    Bestrecommend("C9", critiques3, movie_list3, "minkowski")) + "\n")
print("Movie recommended for C9 with Pearson similarity distance: " + str(
    Bestrecommend("C9", critiques3, movie_list3, "pearson")) + "\n")
print("Movie recommended for C9 with Cosine similarity distance: " + str(
    Bestrecommend("C9", critiques3, movie_list3, "cosine")) + "\n")

print("Question 5:------------------------------------------------")

# generating new ratings that satisfy conditions 1 and 2
# until all similarity metrics output different results
# run this function to generate another result, takes about 1 minute
def find_5_diff_results():
    n_movies = 15
    n_critics = 10
    perc_missing = 0.4
    target_critic=0
    trg_critic = "C"+str(target_critic)
    satisfy = False

    while satisfy == False:
        movies, critiques = generate_ratings(
            n_movies=n_movies, n_critics=n_critics, perc_missing=perc_missing)
        
        c1 = check_missing_data_percentage(movies, critiques)
        c2 = check_chosen_critique(trg_critic, movies, critiques)

        if (c1 == True) and (c2 == True):
            ma = Bestrecommend(trg_critic, critiques, movies, "manhattan")
            eu = Bestrecommend(trg_critic, critiques, movies, "euclidean")
            mi = Bestrecommend(trg_critic, critiques, movies, "minkowski")
            pe = Bestrecommend(trg_critic, critiques, movies, "pearson")
            co = Bestrecommend(trg_critic, critiques, movies, "cosine")
            # print(ma,eu,mi,pe,co)
            
            n_unique = len(set([ma,eu,mi,pe,co]))

            if n_unique == 5:
                satisfy = True
                break
    
    # saving the ratings to excel
    df = pd.DataFrame(critiques)
    df = df.T
    df.to_excel('q5_data.xlsx', index=False)
    

# Testing our current result
file4 = 'q5_data.xlsx'
_, critiques4 = get_data(file4)
movie_list4 = ["M"+str(i) for i in range(15)]

check_missing_data_percentage(movie_list4, critiques4)
check_chosen_critique('C0', movie_list4, critiques4)

print('Critic chosen for recommendation: C0.')
print("Movie recommended for C0 with Manhattan similarity distance: " + str(
    Bestrecommend("C0", critiques4, movie_list4, "manhattan")) + "\n")
print("Movie recommended for C0 with Euclidean similarity distance: " + str(
    Bestrecommend("C0", critiques4, movie_list4, "euclidean")) + "\n")
print("Movie recommended for C0 with Minkowski similarity distance: " + str(
    Bestrecommend("C0", critiques4, movie_list4, "minkowski")) + "\n")
print("Movie recommended for C0 with Pearson similarity distance: " + str(
    Bestrecommend("C0", critiques4, movie_list4, "pearson")) + "\n")
print("Movie recommended for C0 with Cosine similarity distance: " + str(
    Bestrecommend("C0", critiques4, movie_list4, "cosine")) + "\n")