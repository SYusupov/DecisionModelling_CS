import pandas as pd
import numpy as np
import string
import math
import random

## ToDo:
## 1. SimpleMajorityRulefor2
## 2. Manage ties for the functions, mention how you do it in the comments
## 3. Confirm with several examples that functions work correctly

def reading_excel(input):
    """
    read the votes info which is in excel
    input
    - is an excel file where the 1st column: number of voters with the preferences, 2nd to last columns: the order of the preference
    - should not have headers(labels for the nodes) for both columns and rows
    
    matrix_np - the matrix form
    """

    df = pd.read_excel(input, header=None)
    matrix_np = df.to_numpy()

    return matrix_np 

def Plurality(voting_prefs):
    majority_sum = {}

    # calculate sum of the highest preference for each preference
    for pref in voting_prefs:
        cur_n_votes = int(pref[0])
        if pref[1] not in majority_sum:
            majority_sum[pref[1]] = cur_n_votes
        else:
            majority_sum[pref[1]] += cur_n_votes
    
    winner = max(majority_sum, key=majority_sum.get)
    return winner

def PluralityRunoff(voting_prefs):
    voting_prefs_copy = voting_prefs.copy()
    majority_sum = {}
    n_votes = 0

    # calculate sum of the highest preference for each preference
    for pref in voting_prefs_copy:
        cur_n_votes = int(pref[0])
        n_votes += cur_n_votes

        if pref[1] not in majority_sum:
            majority_sum[pref[1]] = cur_n_votes
        else:
            majority_sum[pref[1]] += cur_n_votes

    # get top2 candidates
    sorted_majority = sorted(majority_sum.items(), key=lambda x: x[1], reverse=True)
    top2 = [x[0] for x in sorted_majority[:2]]
    if majority_sum[top2[0]] / n_votes > 0.5:
        return top2[0]

    else:
        ## creating a new array with only the top 2 candidates
        # leaving only top 2 places in the array
        top2_votingPrefs = voting_prefs_copy[:, :3]
        # checking if the top2 candidates are in a cell
        mask = np.isin(voting_prefs_copy, top2)
        # replacing with the top2
        n_prefs = voting_prefs_copy.shape[0]
        top2_votingPrefs[:,1:] = voting_prefs_copy[mask].reshape(n_prefs, 2)
        # get the top candidate
        return Plurality(top2_votingPrefs)

# convert char to equivalent index e.g. a=0, b=1, c=2 ...
def n(char): return ord(char) - 97
    
def Condorrcet(matrix):
    n_votes_col = matrix[:,0].astype(int)
    totalVotes = np.sum(n_votes_col)
    half = np.ceil(totalVotes / 2)
    N = len(matrix[0]) - 1
    counts = np.zeros((N, N))

    # Sum the votes for each pair
    for row in matrix:
        votes = int(row[0])
        for j in range(1, len(row)-1):
            for k in range(j+1, len(row)):
                # print(f'[{row[j]}] [{row[k]}] += {counts[n(row[j])][n(row[k])]}+{votes}')
                counts[n(row[j])][n(row[k])] += votes
        # print('..')

    # Generate matrix of wins over each candidate
    winMatrix = np.where((counts >= half), 1, 0)
    # Sum along rows, the one with all 1 wins (ignoring diagonal)
    sum = np.sum(winMatrix, axis=1)
    winner = -1
    for i, val in enumerate(sum):
        if val == N-1: winner = chr(97 + i)
    
    if winner == -1: return 'No winner'
    return winner

# The function use  a dictionary counts to keep track of counting factor * by votes for each candidate
# and choose the min count as the Borda winner
def BordaVoting(matrix):
    N = len(matrix[0]) - 1
    counts = np.zeros(N)
    for row in matrix:
        votes = int(row[0])
        for j in range(1, len(row)):
            # print(f'[{row[j]}] += {counts[n(row[j])]}+{j}x{votes}')
            counts[n(row[j])] += j * votes
    # print(counts)
    winner = np.argmin(counts)
    return chr(97 + winner)

def generate_PrefSet(n_votes=40, n_candidates = 6):
    """Randomly generating preferences set based on the given number of votes,
    number of candidates, and the 4 conditions"""
    candidates =  list(string.ascii_lowercase)[:n_candidates]

    n_top_candidates = {x:0 for x in candidates} # to record top for condition 4

    voting_prefs = np.empty((0, len(candidates)+1)) # matrix to store prefs
    sum_votes = 0 # n of total votes already made by created preferences

    # for condition 1
    max_pref_vote = math.floor(0.9*n_votes)
    # for condition 2
    max_top_candidate = math.floor(0.7*n_votes)

    while sum_votes < n_votes:
        # generate a new random preference
        satisfy = False
        while satisfy == False:
            # randomly generate the preference order
            pref = random.sample(candidates, len(candidates))
            # randomly select the number of votes, smaller than max
            n_pref_votes = random.randint(1,max_top_candidate)

            # check if the first pref candidate has less than allowed (condition 4)
            if n_top_candidates[pref[0]] + n_pref_votes < max_top_candidate:
                satisfy = True
                n_top_candidates[pref[0]] += n_pref_votes
                voting_prefs = np.vstack((voting_prefs, [n_pref_votes]+pref))
                sum_votes += n_pref_votes

    # reducing the last pref's n so that total equals n_votes
    if sum_votes > n_votes:
        sum_b4_last = sum([int(i) for i in voting_prefs[:-1,0]])
        n_last = n_votes - sum_b4_last
        voting_prefs[-1,0] = str(n_last)
    return voting_prefs

if __name__ == '__main__':
    input = reading_excel('voting_sample.xlsx')
    print(input)
    print(f'Plurality Voting Winner: {Plurality(input)}')
    print(f'PluralityRunoff Voting Winner: {PluralityRunoff(input)}')
    print(f'Condorrcet Voting Winner: {Condorrcet(input)}')
    print(f'BordaVoting Voting Winner: {BordaVoting(input)}')

    ## Question 6
    # Generate until you get the same result for all voting rules
    satisfy = False
    while satisfy == False:
        voting_prefs = generate_PrefSet()
        
        condorrcet_out = Condorrcet(voting_prefs)
        borda_out = BordaVoting(voting_prefs)
        plural_out = Plurality(voting_prefs)
        pluralrun_out = PluralityRunoff(voting_prefs)

        if condorrcet_out == borda_out == plural_out == pluralrun_out:
            satisfy = True
    print('Q6 preferences:\n',voting_prefs)

    ## Question 7
    # Generate until you get different results for all voting rules
    satisfy = False
    while satisfy == False:
        voting_prefs = generate_PrefSet()
        
        condorrcet_out = Condorrcet(voting_prefs)
        borda_out = BordaVoting(voting_prefs)
        plural_out = Plurality(voting_prefs)
        pluralrun_out = PluralityRunoff(voting_prefs)

        if condorrcet_out != borda_out != plural_out != pluralrun_out:
            satisfy = True
    print('Q7 preferences:\n',voting_prefs)