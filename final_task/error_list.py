def is_brackets_balanced(tokens_array):
    brackets_balance_count = 0
    for elem in tokens_array:
        if elem.priority == 0:
            brackets_balance_count += 1
        elif elem.priority == 1:
            brackets_balance_count -= 1
    return brackets_balance_count


def is_operations_missed(tokens_array):
    types = ['operator', 'function']
    for i in range(len(tokens_array)-1):
        if tokens_array[i].type not in types and tokens_array[i+1].type not in types:
            return True
    else:
        return False


def is_operations_ordered(token_array, operations):
    invalid_combinations = {'+', '-', '*', '/', '^', '<', '>', '%'}
    for i, checked_char in enumerate(token_array):
        for operators in operations:
            if str(checked_char.value) in operators and str(token_array[i+1].value) in invalid_combinations:
                print(checked_char)
                return False
    else:
        return True
