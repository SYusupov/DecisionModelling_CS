from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc

import numpy as np

# Function to find optimal threshold using ROC analysis
def find_optimal_threshold(data, labels):
    # Map class labels to integers
    label_mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
    y_true = np.array([label_mapping[label] for label in labels])

    # Split the data into train and test sets
    X_train, _, y_train, _ = train_test_split(data, y_true, test_size=0.01, random_state=42)

    # Compute ROC curve and AUC for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(len(np.unique(y_true))):
        y_true_i = (y_true == i).astype(int)
        fpr[i], tpr[i], _ = roc_curve(y_true_i, data)
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Find the threshold that maximizes the sum of sensitivity and specificity
    optimal_thresholds = np.zeros(len(np.unique(y_true)))
    for i in range(len(np.unique(y_true))):
        optimal_thresholds[i] = X_train[y_train == i].mean()

    return optimal_thresholds

def generate_thresholds(
        df, columns):
    """Getting Thresholds based on the data
        thresholds - should start from border of the best value 
        and end with the worst one, sorted"""
    # 'Energy', 'Sugars',
    #    'Saturated_fatty_acids', 'Salt', 'Proteins', 'Fiber', 'Fruit_vegetable',
    #    'Nutriscore', 'nutriscore_grade'
    labels = df['nutriscore_grade']

    thresholds = {}
    for column in columns:
        data = df[column]

        # Find optimal thresholds
        optimal_threshold = find_optimal_threshold(data, labels)
        thresholds[column] = optimal_threshold
    
    ## Sort the borders either in descending or ascending order
    for key, value in thresholds.items():
        value = [round(v, 2) for v in value]
        thresholds[key] = list(value)

    negative_crits = ['energy','saturated_fat','sugar','salt']
    positive_crits = ['fiber','protein','fruit']

    for column in columns:
        if any(s in column for s in negative_crits):
            thresholds[column].sort()
        elif any(s in column for s in positive_crits):
            thresholds[column].sort(reverse=True)

    return thresholds

def PessimisticmajoritySorting(df, lmd, columns = ['energy_100g', 'saturated-fat_100g', 'sugars_100g', 'fiber_100g',
            'proteins_100g', 'salt_100g', 'fruits-vegetables-nuts_100g'], results_col_1 = 'pessim_electre_lmd=',
            debug=False, weights=None):
    """
    lmd - proportion of weights that a datapoint should be pass to go over the border
    results_col_1 - the name of the column to save the results to
    """
    results_col = f'{results_col_1}{lmd}'
    df[results_col] = ''
    classes = ['a', 'b', 'c', 'd', 'e']
    
    if weights == None:
        weights = {
            "energy_100g":1, "sugars_100g":1, "saturated-fat_100g":1, "salt_100g": 1, 
            "proteins_100g":2, "fiber_100g": 2, "fruits-vegetables-nuts_100g":2}
        # weights = {
        #     "Energy":1, "Sugars":1, "Saturated_fatty_acids":1, "Salt": 1, 
        #     "Proteins":2, "Fiber": 2, "Fruit_vegetable":2}
    weights_sum = sum(weights.values())

    thresholds = generate_thresholds(df, columns)

    criteria = list(thresholds.keys())

    # check if criteria are ascending or descending
    crit_increase = {}
    for criterion in criteria:
        if thresholds[criterion][0] > thresholds[criterion][-1]:
            crit_increase[criterion] = False
        else:
            crit_increase[criterion] = True

    data_idx = 0

    for row_idx, _ in df.iterrows():
        border_idx = 0
        chose_class = False

        while chose_class == False:
            # for each next border comparison, initialize over_border_value
            over_border_value = 0
            for criterion in criteria:
                product_value = df.iloc[data_idx][criterion]
                border_value = thresholds[criterion][border_idx]
                if debug:
                    print(product_value, border_value)
                
                if crit_increase[criterion] == False:
                    # the higher the value, the better
                    if product_value >= border_value:
                        # the value is better than border
                        if debug:
                            print(criterion, 'better 1')
                        over_border_value += weights[criterion]
                else:
                    # the lower the value the better
                    if product_value <= border_value:
                        # the value is better than border
                        if debug: 
                            print(criterion, 'better 2')
                        over_border_value += weights[criterion]
            
            over_border_perc = over_border_value / weights_sum
            if debug:
                print("weight", over_border_perc)

            if over_border_perc >= lmd:
                # product should stay in the class
                chose_class = True
                chosen_class = classes[border_idx]
            else:
                # product should go to the lower class
                border_idx += 1
                # check if it's not the last border
                if border_idx + 1 == len(thresholds[criterion]):
                    # assign the last class because no more borders
                    chose_class = True
                    chosen_class = classes[border_idx]
            if debug:
                print("____Done with this border \n")
        
        if debug:
            print(chosen_class)
            print("________________________________________")
            break

        df.at[row_idx, results_col] = chosen_class
        data_idx+=1
    
    if not debug:
        return df

def OptimisticmajoritySorting(df, lmd, columns = ['energy_100g', 'saturated-fat_100g', 'sugars_100g', 'fiber_100g',
            'proteins_100g', 'salt_100g', 'fruits-vegetables-nuts_100g'], debug=False, weights=None):
    """
    lmd - proportion of weights that a datapoint should be pass to go over the border
    """
    results_col = f'optim_electre_lmd={lmd}'
    df[results_col] = ''
    classes = ['e', 'd', 'c', 'b', 'a']

    if weights == None:
        weights = {
            "energy_100g":1, "sugars_100g":1, "saturated-fat_100g":1, "salt_100g": 1, 
            "proteins_100g":2, "fiber_100g": 2, "fruits-vegetables-nuts_100g":2}
    weights_sum = sum(weights.values())

    thresholds = generate_thresholds(df, columns)
    # threshodls are from the best to the worst
    # so we need to reverse the order first
    thresholds_rev = {key: value[::-1] for key, value in thresholds.items()}

    criteria = list(thresholds_rev.keys())

    # check if criteria are ascending or descending
    crit_increase = {}
    for criterion in criteria:
        if thresholds_rev[criterion][0] > thresholds_rev[criterion][-1]:
            crit_increase[criterion] = False
        else:
            crit_increase[criterion] = True

    data_idx = 0

    for row_idx, _ in df.iterrows():
        border_idx = 0
        
        chose_class = False

        while chose_class == False:
            # for each next border comparison, initialize over_border_value
            over_border_value = 0
            for criterion in criteria:
                product_value = df.iloc[data_idx][criterion]
                border_value = thresholds_rev[criterion][border_idx]
                if debug:
                    print('criterion: ', criterion, product_value, border_value)
                
                if crit_increase[criterion] == True:
                    # the higher the value, the better
                    if border_value <= product_value:
                        # the value is better than border
                        if debug:
                            print(criterion, 'better 1')
                        over_border_value += weights[criterion]
                else:
                    # the lower the value the better
                    if border_value >= product_value:
                        # the value is better than border
                        if debug:
                            print(criterion, 'better 2')
                        over_border_value += weights[criterion]
            
            over_border_perc = over_border_value / weights_sum
            if debug:
                print('weight', over_border_perc)
            if over_border_perc >= lmd:
                # product should go to a better class
                border_idx += 1
                # check if it's not the last border
                if border_idx + 1 == len(thresholds_rev[criterion]):
                    # assign the last class because no more borders
                    chose_class = True
                    chosen_class = classes[border_idx]
            else:
                # product stay in this class
                chose_class = True
                chosen_class = classes[border_idx]
            if debug:
                print("____Done with this border \n")
        
        if debug:
            print(chosen_class)
            print("________________________________________")
            break

        df.at[row_idx, results_col] = chosen_class
        data_idx+=1
    if not debug:
        return df