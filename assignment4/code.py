import math

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
            # print("m1m2", person1[movie], person2[movie])
            euclidienne_dist += (person1[movie] - person2[movie]) ** 2
            # print("ed", euclidienne_dist)
    return math.sqrt(euclidienne_dist)

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
    denominator = math.sqrt(sum_x2 - (sum_x ** 2) / n) * math.sqrt(sum_y2 - (sum_y ** 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator


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

    # Generating new movies' list
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
            
            elif similarity_function == "pearson":
                distanceOfCritique = sim_distancePearson(Critiques[nouveauCritique], Critiques[critique])
                s += (1 + distanceOfCritique)
                total += (nouveauMovieRating * (1 + distanceOfCritique))
            
            elif similarity_function == "cosine":
                distanceOfCritique = sim_distanceCosine(Critiques[nouveauCritique], Critiques[critique])
                s += (1 + distanceOfCritique)
                total += (nouveauMovieRating * (1 + distanceOfCritique))

        s_dash = total / s
        
        if s_dash > max_s_dash:
            max_s_dash = s_dash
            movieRecommended = movie

    return movieRecommended

print('----------------------------------------------------')
print('Example 1:------------------------------------------')
print('----------------------------------------------------')

movie_list1 = ["Lady", "Snake", "Luck", "Superman", "Dupree", "Night"]
critiques1 = {"Lisa Rose": {'Lady': 2.5, 'Snake': 3.5, 'Luck': 3.0, 'Superman': 3.5, 'Dupree': 2.5, 'Night': 3.0},
              "Gene Seymour": {'Lady': 3.0, 'Snake': 3.5, 'Luck': 1.5, 'Superman': 5.0, 'Dupree': 3.5,
                               'Night': 3.0},
              "Michael Phillips": {'Lady': 2.5, 'Snake': 3.0, 'Superman': 3.5, 'Night': 4.0},
              "Claudia Puig": {'Snake': 3.5, 'Luck': 3.0, 'Superman': 4.0, 'Dupree': 2.5, 'Night': 4.5},
              "Mick Lasalle": {'Lady': 3.0, 'Snake': 4.0, 'Luck': 2.0, 'Superman': 3.0, 'Dupree': 2.0,
                               'Night': 3.0},
              "Jack Matthews": {'Lady': 3.0, 'Snake': 4.0, 'Superman': 5.0, 'Dupree': 3.5, 'Night': 3.0},
              "Toby": {'Snake': 4.5, 'Superman': 4.0, 'Dupree': 1.0},
              "Anne": {'Lady': 1.5, 'Luck': 4.0, 'Dupree': 2.0}
              }

print("Eucleadian between Lisa and Gene: ", sim_distanceEuclidienne(critiques1["Lisa Rose"], critiques1["Gene Seymour"]))

print("Movie recommended for Anne with Manhattan similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "manhattan")) + "\n")
print("Movie recommended for Anne with Euclidean similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "euclidean")) + "\n")
print("Movie recommended for Anne with Pearson similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "pearson")) + "\n")
print("Movie recommended for Anne with Cosine similarity distance: " + str(
    Bestrecommend("Anne", critiques1, movie_list1, "cosine")) + "\n")

movie_list2 = ["Blues Traveler", "Broken Bells", "Deadmau5", "Norah Jones", "Phoenix", "Slightly Stoopid",
               "The Strokes", "Vampire Weekend"]
critiques2 = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0, "Norah Jones": 4.5, "Phoenix": 5.0,
                           "Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0},
              "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0,
                       "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0},
              "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0,
                       "Phoenix": 5.0, "Slightly Stoopid": 1.0},
              "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0,
                      "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0},
              "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0,
                         "Vampire Weekend": 1.0},
              "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0,
                         "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0},
              "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0,
                      "Slightly Stoopid": 4.0, "The Strokes": 5.0},
              "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5,
                           "The Strokes": 3.0}
              }

print('----------------------------------------------------')
print('Example 2:------------------------------------------')
print('----------------------------------------------------')

print('\nFor Veronica:---------------------------------------')
print("Movie recommended for Veronica with Manhattan similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "manhattan")) + "\n")
print("Movie recommended for Veronica with Euclidean similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "euclidean")) + "\n")
print("Movie recommended for Veronica with Pearson similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "pearson")) + "\n")
print("Movie recommended for Veronica with Cosine similarity distance: " + str(
    Bestrecommend("Veronica", critiques2, movie_list2, "cosine")) + "\n")

print('\nFor Hailey:----------------------------------------')
print("Movie recommended for Hailey with Manhattan similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "manhattan")) + "\n")
print("Movie recommended for Hailey with Euclidean similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "euclidean")) + "\n")
print("Movie recommended for Hailey with Pearson similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "pearson")) + "\n")
print("Movie recommended for Hailey with Cosine similarity distance: " + str(
    Bestrecommend("Hailey", critiques2, movie_list2, "cosine")) + "\n")