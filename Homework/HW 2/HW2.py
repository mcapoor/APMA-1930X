# APMA 1930X: Homework 2
# Author: Milan Capoor
# Date: 4 October 2024

# ------------------------- PROBLEM 1 -------------------------
# PROBLEM 1 STATEMENT

# Input: 
# - denominations: List[Int], List of distinct positive integers whose first element is always 1
# - sum: Int, positive integer

# Output:
# - count: Int, smallest number of elements from a_n that sum to x
# - elements: List[Int], list of number of each denomination used to sum to x

# Given tests:
p1_test1_input = {'denominations': [1, 7, 10], 'sum': 14}
p1_test1_output = {'count': 2, 'elements': [0, 2, 0]}

p1_test2_input = {'denominations': [1, 5, 10, 25], 'sum': 51}
p1_test2_output = {'count': 3, 'elements': [1, 0, 0, 2]}

p1_test3_input = {'denominations': [1, 7, 10], 'sum': 14}
p1_test3_output = {'count': 2, 'elements': [0, 2, 0]}

p1_test4_input = {'denominations': [1, 7, 10], 'sum': 25}
p1_test4_output = {'count': 4, 'elements': [1, 2, 1]}

# Evaluation questions:
p1_question1_input = {'denominations': [1, 6, 10], 'sum': 13}

p1_question2_input = {'denominations': [1, 1930, 2023], 'sum': 10**6}

# PROBLEM 1 SOLUTION

def problem_1(test: dict) -> dict:
    denominations = test['denominations']
    target_sum = test['sum']
        
    # Initialize (denominations x target_sum) array
    optimal_value_table = [[None for _ in range(target_sum + 1)] for _ in range(len(denominations))]

    # Base case: only allowed coins with value 1 
    optimal_value_table[0] = [{'count': target, 'elements': [target] + [0 for _ in range(1, len(denominations))]} 
                                for target in range(target_sum + 1)]

    # Inductive step 
    for index in range(1, len(denominations)):
        for target in range(target_sum + 1): 
            coin_value = denominations[index]
            previous_state = optimal_value_table[index - 1][target]

            if coin_value > target:
                optimal_value_table[index][target] = previous_state
            else: 
                value_with_new_coin = optimal_value_table[index][target - coin_value]

                if value_with_new_coin['count'] + 1 < previous_state['count']:
                    coins_list = value_with_new_coin['elements']
                    updated_coins_list = [coin + 1 if i == index else coin for i, coin in enumerate(coins_list)]

                    optimal_value_table[index][target] = {'count': value_with_new_coin['count'] + 1, 
                                                            'elements': updated_coins_list}
                else: 
                    optimal_value_table[index][target] = previous_state

    potential_combinations = [row[-1] for row in optimal_value_table]
    induction_results = min(potential_combinations, key=lambda x: x['count'])

    return {'count': induction_results['count'], 'elements': induction_results['elements']}

def run_p1_tests(problem_1) -> None:
    if problem_1(p1_test1_input) == p1_test1_output:
        print("Test 1 passed")
    else:
        print("Test 1 failed")
        print(f"Expected: {p1_test1_output}, Returned: {problem_1(p1_test1_input)}\n")

    if problem_1(p1_test2_input) == p1_test2_output:
        print("Test 2 passed")
    else:
        print("Test 2 failed")
        print(f"Expected: {p1_test2_output}, Returned: {problem_1(p1_test2_input)}\n")

    if problem_1(p1_test3_input) == p1_test3_output:
        print("Test 3 passed")
    else:
        print("Test 3 failed")
        print(f"Expected: {p1_test3_output}, Returned: {problem_1(p1_test3_input)}\n")

    if problem_1(p1_test4_input) == p1_test4_output:
        print("Test 4 passed")
    else:
        print("Test 4 failed")
        print(f"Expected: {p1_test4_output}, Returned: {problem_1(p1_test4_input)}\n")

def run_p1_questions(problem_1) -> None:
    print("Evaluation questions:")
    print(f"Q1 Input: {p1_question1_input}, Returned: {problem_1(p1_question1_input)}")
    print(f"Q2 Input: {p1_question2_input}, Returned: {problem_1(p1_question2_input)}")

# PROBLEM 1 OUTPUT

run_p1_tests(problem_1) 
run_p1_questions(problem_1)

# ------------------------- PROBLEM 2 -------------------------
# PROBLEM 2 STATEMENT

# Input:
# - subsequence_1: List[Int], List of digits [0-9] 
# - subsequence_2: List[Int], List of digits [0-9]

# Output: 
# - max_length: Int, length of the longest common subsequence (not necessarily consecutive) between subsequence_1 and subsequence_2
# - longest_subsequence: List[Int], longest common subsequence between subsequence_1 and subsequence_2

# Given tests:
p2_test1_input = {'subsequence_1': [1, 3, 9, 6, 7, 2, 1, 8, 5, 4],
                  'subsequence_2': [3, 0, 8, 9, 2]}
p2_test1_output = {'max_length': 3, 'longest_subsequence': [3, 9, 2]}

# Evaluation questions: 
p2_question1_input = {'subsequence_1': [1, 3, 9, 6, 7, 2, 1, 8, 5, 4],
                      'subsequence_2': [3, 0, 4, 3, 5, 9, 2, 6, 1, 1, 8, 0]}

# PROBLEM 2 SOLUTION

def problem_2(test: dict) -> dict:
    shorter_sequence = test['subsequence_1'] if len(test['subsequence_1']) < len(test['subsequence_2']) else test['subsequence_2']
    longer_sequence = test['subsequence_1'] if len(test['subsequence_1']) >= len(test['subsequence_2']) else test['subsequence_2']

    # Initialize (shorter_sequence x longer_sequence) array
    optimal_value_table = [[0 for _ in range(len(longer_sequence))] for _ in range(len(shorter_sequence))]
    longest_list_table = [[[] for _ in range(len(longer_sequence))] for _ in range(len(shorter_sequence))]

    #Base case
    for j in range(len(longer_sequence)):
        if shorter_sequence[0] in longer_sequence[:j+1]:
            optimal_value_table[0][j] = 1
            longest_list_table[0][j] = [longer_sequence[j]]
        else:
            optimal_value_table[0][j] = 0
            longest_list_table[0][j] = []

    for i in range(len(shorter_sequence)):
        if longer_sequence[0] in shorter_sequence[:i+1]:
            optimal_value_table[i][0] = 1
            longest_list_table[i][0] = [longer_sequence[0]]

    # Inductive step
    for i in range(1, len(shorter_sequence)):
        for j in range(1, len(longer_sequence)):
            if shorter_sequence[i] == longer_sequence[j]:
                if optimal_value_table[i - 1][j] + 1 > optimal_value_table[i][j-1]:
                    optimal_value_table[i][j] = optimal_value_table[i-1][j] + 1
                    longest_list_table[i][j] = longest_list_table[i-1][j] + [longer_sequence[j]]
                else:
                    optimal_value_table[i][j] = optimal_value_table[i][j-1]
                    longest_list_table[i][j] = longest_list_table[i][j-1]
            else:
                if optimal_value_table[i - 1][j] > optimal_value_table[i][j-1]:
                    optimal_value_table[i][j] = optimal_value_table[i - 1][j]
                    longest_list_table[i][j] = longest_list_table[i-1][j]
                else:
                    optimal_value_table[i][j] = optimal_value_table[i][j-1]
                    longest_list_table[i][j] = longest_list_table[i][j-1]

    return {'max_length': optimal_value_table[-1][-1], 'longest_subsequence': longest_list_table[-1][-1]}
    
# PROBLEM 2 OUTPUT

def run_p2_tests(problem_2) -> None:
    if problem_2(p2_test1_input) == p2_test1_output:
        print("Test 1 passed")
    else:
        print("Test 1 failed")
        print(f"Expected: {p2_test1_output}, Returned: {problem_2(p2_test1_input)}\n")

def run_p2_questions(problem_2) -> None:
    print("Evaluation questions:")
    print(f"Q1 Input: {p2_question1_input}, Returned: {problem_2(p2_question1_input)}")

run_p2_tests(problem_2)
run_p2_questions(problem_2)