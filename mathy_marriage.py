import random
# random.seed(10)

class Operation:
    def __init__(self, function, name):
        self.function = function
        self.name = name

    def __str__(self):
        return self.name

    def apply(self, x, y):
        return self.function(x, y)

class Woman:
    def __init__(self, value, string_representation, index):
        self.value = value
        self.string = string_representation
        self.matched = None
        self.index = index
    
    @classmethod
    def copy(cls, prev_woman, operation, num):
        value = operation.apply(prev_woman.value, num)
        if ' ' in prev_woman.string:
            string = '({0}) {1} {2}'.format(prev_woman.string, operation.name, num)
        else:
            string = '{0} {1} {2}'.format(prev_woman.string, operation.name, num)
        return Woman(value, string, prev_woman.index)

    def __str__(self):
        return 'women {0} matched with man {1}: {2}'.format(self.index, self.matched, self.string)


operations = [
                Operation(lambda x, y: x + y, "+"),
                Operation(lambda x, y: x * y, "*"),
                Operation(lambda x, y: x - y, "-"),
                Operation(lambda x, y: x // y, "//"),
                # Operation(lambda x, y: x ** y, "**"),
             ]

# We will say True if a solution exists, and False otherwise

def helper(women, men, numbers):
    """
    # IDEA: We will look at every single possible first "move"
    We will look at every pair of numbers, and every operation between those two numbers
    then, using recursion, we will have a 3 element list, and then use magic!
    """
    assert len(women) == len(men)
    # SUCCESS CASE
    index = None

    # go through each woman, and find the first unmatched woman
    for i, w in enumerate(women):
        if w.matched is not None:
            continue
        elif w.value in men:
            man_index = men.index(w.value)
            w.matched = man_index
            men[man_index] = None    
        else:
            index = i
            break

    if index is None:
        yield "\n".join([str(w) for w in women])
        return

    # FAILURE CASE
    if not numbers:
        return

    # let us iterate first through every number and operation
    for j in range(len(numbers)):
        w = women[index]
        num = numbers[j]
        for operation in operations:
            try:
                new_w = Woman.copy(w, operation, num)
                modified_women = women[:index] + [new_w] + women[index + 1:]
                modified_nums = numbers[:j] + numbers[j + 1:]
                yield from helper(modified_women, men[:], modified_nums)
            except ZeroDivisionError:
                continue

def generate_randomly2(length=4):
    options = 0
    ctr = 0
    sols = 0
    while sols == 0 or sols > 20:
        ctr += 1
        numbers = [random.randint(2, 8) for _ in range(2 * length - length // 2)]
        women = [random.randint(1, 25) for _ in range(length)]
        men = [random.randint(1, 25) for _ in range(length)]

        w, m, n = women[:], men[:], numbers[:]
        sols = len(set(helper(preprocess(w, m), m, n)))
        print("ctr: ", ctr, "| solutions: ", sols)

    return women, men, numbers

def generate_randomly(length=4):
    options = 0
    ctr = 0
    sols = 100
    while ctr < 10 and sols > 20:
        ctr += 1
        numbers = [random.randint(2, 8) for _ in range(2 * length - length // 2)]
        women = [random.randint(1, 25) for _ in range(length)]
        men = women[:]
        # print(men)

        for num in numbers:
            man_index = random.randint(0, length - 1)
            man = men[man_index]
            men[man_index] = random.choice(operations).apply(man, num) 
            # print(men)

        w, m, n = women[:], men[:], numbers[:]
        sols = len(set(helper(preprocess(w, m), m, n)))
        print("solutions", sols)

    return women, men, numbers

def preprocess(women, men):
    women = [Woman(x, str(x), i) for i, x in enumerate(women)]
    for i, w in enumerate(women):
        if w.value in men:
            man_index = men.index(w.value)
            women = women[:]
            new_w = Woman(w.value, w.string, w.index)
            new_w.matched = man_index
            women[i] = new_w
            men[man_index] = None
    return women
    
def solve(women, men, numbers):
    print('-' * 10)
    print("women: ", women)
    print("men:", men)
    print("numbers:", numbers)    
    # preprocessing step, if any men are already equal, match them!
    
    print("Possible solutions: ")
    for ans in set(helper(preprocess(women, men), men, numbers)):
        print(ans)
        print() 
    print('-' * 10)


solve(*generate_randomly2())
# solve([10, 5, 15], [11, 15, 33], [8, 7, 1])
