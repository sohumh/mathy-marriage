# Mathy Marriage

Each puzzle consists of a list of `women`, `men`, and `numbers`, where the `women` and `men` are numbers themselves. The goal is to apply arithmetic operations on `women` using numbers from `numbers` so that each woman is changed to be equal to one unique man. A number in `numbers` can be used only once.

Finally, the arithmetic operations consist of:
- addition
- subtraction
- multiplication
- division (must divide cleanly)

Each arithmetic operation must be applied to the woman, e.g. `operation_two(operation_one(woman, num_one), num_two)`. 

Admittedly, this may appear a bit confusing, so let's see an example! Suppose we have the women, men, and numbers below:
```python
women:  [19, 15, 22]
men: [20, 2, 3]
numbers: [4, 2, 5, 4, 5]
```

Then, a possible solution is the following:
```ruby
woman 19 matched with man 2: ((19 + 5) / 4) - 4
woman 15 matched with man 3: 15 / 5
woman 22 matched with man 20: 22 - 2
```

Observe that:
- Each number in `numbers` is used at most once, e.g. the only time the `2` is used is in the operation `22 - 2`. Most solutions will require all to be used, but some may not!
- Each woman is matched to a unique man who doesn't necessarily appear at the same index as her. 

To see some challenges, visit [sohumh.github.io/projects/mathy_marriage](https://sohumh.github.io/projects/mathy_marriage/)
