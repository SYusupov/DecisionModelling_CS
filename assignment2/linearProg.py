from pulp import *

# the rankings
durations = {
    'Arc_de_Triomphe': 1,
    'Avenue_des_Champs_Elysees': 1.5,
    'Basilique_du_Sacre_Coeur': 2,
    'Catacombes': 2,
    'Cathedrale_Notre_Dame': 2,
    'Centre_Pompidou': 2.5,
    'Eiffel_Tower': 4.5,
    'Jardin_Tuileries': 1.5,
    'Museum_Louvre': 3,
    'Museum_Orsay': 2,
    'Place_de_la_Concorde': 0.75,
    'Sainte_Chapelle': 1.5,
    'Tour_Montparnasse': 2
}
prices = {
    'Arc_de_Triomphe': 9.5,
    'Avenue_des_Champs_Elysees': 0,
    'Basilique_du_Sacre_Coeur': 8,
    'Catacombes': 10,
    'Cathedrale_Notre_Dame': 5,
    'Centre_Pompidou': 10,
    'Eiffel_Tower': 15.5,
    'Jardin_Tuileries': 0,
    'Museum_Louvre': 12,
    'Museum_Orsay': 11,
    'Place_de_la_Concorde': 0,
    'Sainte_Chapelle': 8.5,
    'Tour_Montparnasse': 15
}

appreciations = {
    'Arc_de_Triomphe': 3,
    'Avenue_des_Champs_Elysees': 5,
    'Basilique_du_Sacre_Coeur': 4,
    'Catacombes': 4,
    'Cathedrale_Notre_Dame': 5,
    'Centre_Pompidou': 1,
    'Eiffel_Tower': 5,
    'Jardin_Tuileries': 3,
    'Museum_Louvre': 4,
    'Museum_Orsay': 2,
    'Place_de_la_Concorde': 3,
    'Sainte_Chapelle': 1,
    'Tour_Montparnasse': 2
}

def calculate_variables(prices, durations, prob):
    """Calculates duration and price of the given visit"""
    ListVisit = []
    for v in prob.variables():
        if v.varValue == 1 and v.name in prices.keys():
            ListVisit.append(v.name)

    print("Total number of places visited = ", int(value(prob.objective)))
    print("The places visited: ", ", ".join([f"{x}" for x in ListVisit]))

    print("Total money spent: ",sum([prices[v] for v in ListVisit]))
    print("Total time spent: ",sum([durations[v] for v in ListVisit]))
    return ListVisit

print("-------------------Section 1-------------------")

# defining that all attractions can be visited once or not at all
TE = LpVariable("Eiffel_Tower",0,1,LpInteger)
ML = LpVariable("Museum_Louvre",0,1,LpInteger)
AT = LpVariable("Arc_de_Triomphe",0,1,LpInteger)
MO = LpVariable("Museum_Orsay",0,1,LpInteger)
JT = LpVariable("Jardin_Tuileries",0,1,LpInteger)
CA = LpVariable("Catacombes",0,1,LpInteger)
CP = LpVariable("Centre_Pompidou",0,1,LpInteger)
CN = LpVariable("Cathedrale_Notre_Dame",0,1,LpInteger)
BS = LpVariable("Basilique_du_Sacre_Coeur",0,1,LpInteger)
SC = LpVariable("Sainte_Chapelle",0,1,LpInteger)
PC = LpVariable("Place_de_la_Concorde",0,1,LpInteger)
TM = LpVariable("Tour_Montparnasse",0,1,LpInteger)
AC = LpVariable("Avenue_des_Champs_Elysees",0,1,LpInteger)

def create_InitState():
    """Initiating the linear programming problem with the default objective function
    and the constraints, used throughout Section 1 and 2"""
    prob = LpProblem("Visiting_Paris", LpMaximize)

    # The objective function
    prob += TE+ML+AT+MO+JT+CA+CP+CN+BS+SC+PC+TM+AC # the sum of all visits of sites

    # The constraints
    prob += 4.5*TE+3*ML+1*AT+2*MO+1.5*JT+2*CA+2.5*CP+2*CN+2*BS+1.5*SC+0.75*PC+2*TM+1.5*AC<=12
    prob += 15.5*TE+12*ML+9.5*AT+11*MO+10*CA+10*CP+5*CN+8*BS+8.5*SC+15*TM<=65
    return prob

prob = create_InitState()
prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])
ListVisit1 = calculate_variables(prices, durations, prob)
print("\n")

print("-------------------Section 2-------------------")
print("\n")

print("------------------Preference 1-----------------")

prob = create_InitState()

# or operator for each pair that is within 1 km
MO_JT = pulp.LpVariable("MO_JT", 0, 1, LpInteger)
CP_CN = pulp.LpVariable("CP_CN", 0, 1, LpInteger) 
ML_SC = pulp.LpVariable("ML_SC", 0, 1, LpInteger)
SC_CP = pulp.LpVariable("SC_CP", 0, 1, LpInteger)
CN_SC = pulp.LpVariable("CN_SC", 0, 1, LpInteger)
PC_MO = pulp.LpVariable("PC_MO", 0, 1, LpInteger)
PC_JT = pulp.LpVariable("PC_JT", 0, 1, LpInteger)
AT_AC = pulp.LpVariable("AT_AC", 0, 1, LpInteger)

# If MO + JT is 0, ML_CP must be 0. If ML + CP is 2, ML_CP must be 1.
pref1 = [
    MO + JT == 2 * MO_JT, CP + CN == 2 * CP_CN, ML + SC == 2 * ML_SC, 
    SC + CP == 2 * SC_CP, CN + SC == 2 * CN_SC, PC + MO == 2 * PC_MO, 
    PC + JT == 2 * PC_JT, AT + AC == 2 * AT_AC]

for constr in pref1:
    prob += constr

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit2 = calculate_variables(prices, durations, prob)
print("Same as ListVisit1: ", ListVisit1==ListVisit2)
print("\n")

print("------------------Preference 2-----------------")

prob = create_InitState()

# The preference
pref2 = [TE+CA == 2]

for constr in pref2:
    prob += constr

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit3 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit3!=ListVisit1)
print("\n")

print("------------------Preference 3-----------------")

prob = create_InitState()

pref3 = [CN+SC<=1]
for constr in pref3:
    prob +=  constr

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit4 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit4!=ListVisit1)
print("\n")

print("------------------Preference 4-----------------")

prob = create_InitState()

# The preference
pref4 = [TM == 1]
for constr in pref4:
    prob += constr

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit5 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit5!=ListVisit1)
print("\n")

print("------------------Preference 5-----------------")

prob = create_InitState()

# representing the OR condition
ML_CP = pulp.LpVariable("ML_CP", 0, 1, LpInteger)

# The preference
pref5 = [ML + CP == 2 * ML_CP] 
for constr in pref5:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit6 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit6!=ListVisit1)
print("\n")

print("----------------Preferences 1,2----------------")

prob = create_InitState()

# The preference
for constr in pref1+pref2:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit1_2 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit1_2!=ListVisit1)
print("\n")

print("----------------Preferences 1,3----------------")

prob = create_InitState()

# The preference
for constr in pref1+pref3:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit1_3 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit1_3!=ListVisit1)
print("\n")

print("----------------Preferences 1,4----------------")
prob = create_InitState()

# The preference
for constr in pref1+pref4:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit1_4 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit1_4!=ListVisit1)
print("\n")

print("----------------Preferences 2,5----------------")
prob = create_InitState()

# The preference
for constr in pref2+pref5:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])
ListVisit2_5 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit2_5!=ListVisit1)
print("\n")

print("----------------Preferences 3,4----------------")
prob = create_InitState()

# The preference
for constr in pref3+pref4:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit3_4 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit3_4!=ListVisit1)
print("\n")

print("----------------Preferences 4,5----------------")
prob = create_InitState()

# The preference
for constr in pref4+pref5:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit4_5 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit4_5!=ListVisit1)
print("\n")

print("----------------Preferences 1,2,4----------------")
prob = create_InitState()

# The preference
for constr in pref2+pref1+pref4:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit1_2_4 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit1_2_4!=ListVisit1)
print("\n")

print("----------------Preferences 2,3,5----------------")
prob = create_InitState()

# The preference
for constr in pref2+pref5+pref3:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit2_3_5 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit2_3_5!=ListVisit1)
print("\n")

print("----------------Preferences 2,3,4,5----------------")
prob = create_InitState()

# The preference
for constr in pref2+pref5+pref3+pref4:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])
ListVisit2_3_4_5 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit2_3_4_5!=ListVisit1)
print("\n")

print("----------------Preferences 1,2,4,5----------------")
prob = create_InitState()

# The preference
for constr in pref2+pref5+pref1+pref4:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit1_2_4_5 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit1_2_4_5!=ListVisit1)
print("\n")

print("----------------Preferences 1,2,3,4,5----------------")
prob = create_InitState()

# The preference
for constr in pref1+pref2+pref3+pref4+pref5:
    prob += constr 

prob.solve(PULP_CBC_CMD(msg=False))
print("Status: ",LpStatus[prob.status])

ListVisit1_2_3_4_5 = calculate_variables(prices, durations, prob)
print("Different from ListVisit1: ", ListVisit1_2_3_4_5!=ListVisit1)
print("\n")

print("-------------------Section 3-------------------")

from scipy.stats import kendalltau, spearmanr

# reversing the order because the higher the ranking the better
# while for both price and duration, the less the better
appreciations = {i:j*(-1) for i, j in appreciations.items()} 
print(appreciations)

kendall = kendalltau(list(durations.values()), list(prices.values())).correlation
spearman = spearmanr(list(durations.values()), list(prices.values())).correlation
print(
    'Duration and Prices, kendall:', round(kendall,3), 
    ', spearman:', round(spearman, 3))

kendall = kendalltau(list(durations.values()), list(appreciations.values())).correlation
spearman = spearmanr(list(durations.values()), list(appreciations.values())).correlation
print(
    'Duration and Appreciations, kendall:', round(kendall,3), 
    ', spearman:', round(spearman, 3))

kendall = kendalltau(list(prices.values()), list(appreciations.values())).correlation
spearman = spearmanr(list(prices.values()), list(appreciations.values())).correlation
print(
    'Prices and Appreciations, kendall:', round(kendall,3), 
    ', spearman:', round(spearman, 3))