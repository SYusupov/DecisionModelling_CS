import pandas as pd
import numpy as np

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
        if pref[1] not in majority_sum:
            majority_sum[pref[1]] = pref[0]
        else:
            majority_sum[pref[1]] += pref[0]
    
    winner = max(majority_sum, key=majority_sum.get)
    return winner

def PluralityRunoff(voting_prefs):
    majority_sum = {}
    n_votes = 0

    # calculate sum of the highest preference for each preference
    for pref in voting_prefs:
        n_votes += pref[0]

        if pref[1] not in majority_sum:
            majority_sum[pref[1]] = pref[0]
        else:
            majority_sum[pref[1]] += pref[0]

    # get top2 candidates
    sorted_majority = sorted(majority_sum.items(), key=lambda x: x[1], reverse=True)
    top2 = [x[0] for x in sorted_majority[:2]]
    if majority_sum[top2[0]] / n_votes > 0.5:
        return top2[0]

    else:
        ## creating a new array with only the top 2 candidates
        # leaving only top 2 places in the array
        top2_votingPrefs = voting_prefs[:, :3]
        # checking if the top2 candidates are in a cell
        mask = np.isin(voting_prefs, top2)
        # replacing with the top2
        n_prefs = voting_prefs.shape[0]
        top2_votingPrefs[:,1:] = voting_prefs[mask].reshape(n_prefs, 2)
        print(top2_votingPrefs)
        # get the top candidate
        return Plurality(top2_votingPrefs)

# convert char to equivalent index e.g. a=0, b=1, c=2 ...
def n(char): return ord(char) - 97
    
def Condorrcet(matrix):
    totalVotes = np.sum(matrix[:,0])
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

def BordaVoting(matrix):
    N = len(matrix[0]) - 1
    counts = np.zeros(N)
    for row in matrix:
        votes = int(row[0])
        for j in range(1, len(row)):
            # print(f'[{row[j]}] += {counts[n(row[j])]}+{(n(row[j])+1)}x{votes}')
            counts[n(row[j])] += (n(row[j])+1) * votes
    # print(counts)
    winner = np.argmin(counts)
    return chr(97 + winner)

if __name__ == '__main__':
    input = reading_excel('voting_sample.xlsx')
    print(input)
    print(f'Plurality Voting Winner: {Plurality(input)}')
    print(f'PluralityRunoff Voting Winner: {PluralityRunoff(input)}')
    print(f'Condorrcet Voting Winner: {Condorrcet(input)}')
    print(f'BordaVoting Voting Winner: {BordaVoting(input)}')