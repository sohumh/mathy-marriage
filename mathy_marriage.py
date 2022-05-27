"""
An algorithm for randomly generating and solving 
(inefficiently) mathy marriage problems
"""

import random
random.seed(11)

class Operation:
    def __init__(self, function, name):
        self.function = function
        self.name = name

    def __str__(self):
        return self.name

    def apply(self, x, y):
        return self.function(x, y)

class Woman:
    def __init__(self, value, string_representation, index, original_value=None):
        self.value = value
        self.string = string_representation
        self.matched = None
        self.index = index
        if original_value == None:
            self.original_value = value
        else:
            self.original_value = original_value
    
    @classmethod
    def copy(cls, prev_woman, operation, num):
        if operation.name == "/" and prev_woman.value % num != 0:
            raise ZeroDivisionError 
        value = operation.apply(prev_woman.value, num)
        if ' ' in prev_woman.string:
            string = '({0}) {1} {2}'.format(prev_woman.string, operation.name, num)
        else:
            string = '{0} {1} {2}'.format(prev_woman.string, operation.name, num)
        return Woman(value, string, prev_woman.index, original_value=prev_woman.original_value)

    def __str__(self):
        return 'woman {0} matched with man {1}: {2}'.format(self.original_value, self.value, self.string)


operations = [
                Operation(lambda x, y: x + y, "+"),
                Operation(lambda x, y: x * y, "*"),
                Operation(lambda x, y: x - y, "-"),
                Operation(lambda x, y: x // y, "/"),
                # Operation(lambda x, y: x ** y, "**"),
             ]

def helper(women, men, numbers):
    assert len(women) == len(men)

    # SUCCESS CASE
    index = None
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

def generate_between_25(length=3, nums_length=4):
    ctr, sols = 0, 0
    while sols != 1:
        ctr += 1
        numbers = random.choices(list(range(1, 8)), k = nums_length)
        options = list(range(1, 25))
        random.shuffle(options)
        women = options[:length]
        men = options[length:length * 2]

        w, m, n = women[:], men[:], numbers[:]
        sols = len(set(helper(preprocess(w, m), m, n)))

    return women, men, numbers

def generate_men_through_operations(length=2):
    ctr = 0
    sols = 100
    while ctr < 10 and sols > 20:
        ctr += 1
        numbers = [random.randint(2, 8) for _ in range(length * 2)]
        women = [random.randint(1, 25) for _ in range(length)]
        men = women[:]

        for num in numbers:
            man_index = random.randint(0, length - 1)
            man = men[man_index]
            men[man_index] = random.choice(operations).apply(man, num) 

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
    print("Solution: ")
    for ans in set(helper(preprocess(women, men), men, numbers)):
        print(ans)
        print() 
    print('-' * 10)

def website_solve(women, men, numbers, i):
    print('**Puzzle {}:**'.format(i))
    print('```python')
    print('women: ', women)
    print('men: ', men)
    print('numbers: ', numbers)
    print('```')
    print('<details>') 
    print('<summary>')
    print('Solution:')
    print('</summary>')
    print()
    print('{% highlight ruby %}')
    for ans in set(helper(preprocess(women, men), men, numbers)):
        print(ans)
    print('{% endhighlight %}')
    print()
    print('</details>') 
    print('---')
    print()

for i in range(1, 11):
    website_solve(*generate_between_25(2, 3), i)
