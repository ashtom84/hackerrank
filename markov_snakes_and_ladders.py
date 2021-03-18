import random

class Game:
    endpoint, maxturns = 100, 1e3
    
    def __init__(self, pos_=1, ladders_=[], snakes_=[], probas_=[1/6 for _ in range(6)], count_=0):
        self.pos = pos_
        self.ladders = ladders_
        self.snakes = snakes_
        self.probas = probas_
        self.count = count_
        
    def cumsum(self, arr):
        c, s = [], 0
        for x in arr:
            s += x
            c.append(s)
        return c
    
    def roll(self):
        '''returns the result of the roll of the die given its probabilities'''
        p = random.random()
        a = self.cumsum(self.probas)
        for i in range(6):
            if p < a[i]:
                return i+1
        return 6

    def check_override(self, pos, overrides):
        for start, end in overrides:
            if pos == start:
                return end
        return None
    
    def turn(self):
        '''simulate a turn of the game: roll a die, update the position'''
        new = self.pos + self.roll()
        self.count += 1
        ladder = self.check_override(new, self.ladders)
        snake = self.check_override(new, self.snakes)
        if ladder is not None:
            self.pos = ladder
        elif snake is not None:
            self.pos = snake
        elif new <= self.endpoint:
            self.pos = new
        
    def play(self):
        '''play the game until reaching the endpoint or doing more rolls than allowed'''
        while self.pos != self.endpoint and self.count < self.maxturns:
            self.turn()
        return self.count
            
    
class Simulate:
    total_simulations = 5e3 + 400
    
    def __init__(self, n_simulations_=0, ladders_=[], snakes_=[], probas_=[1/6 for _ in range(6)]):
        self.n_simulations = n_simulations_
        self.ladders = ladders_
        self.snakes = snakes_
        self.probas = probas_
    
    def run(self):
        '''run a simulation to approximate the expected number of rolls required to get to the endpoint'''
        expectations = []
        while self.n_simulations < self.total_simulations:
            game = Game(ladders_=self.ladders, snakes_=self.snakes, probas_=self.probas)
            expectations.append(game.play())
            self.n_simulations += 1
        return sum(expectations)/len(expectations)


Configurations = []

T = int(raw_input()) # number of tests
config = {}
for _ in range(T):
    config['probas'] = list(map(float, raw_input().strip().split(",")))
    config['n_ls'] = list(map(int, raw_input().strip().split(",")))
    config['ladders'] = [tuple(map(int, x.split(","))) for x in raw_input().split(" ")]
    config['snakes'] = [tuple(map(int, x.split(","))) for x in raw_input().split(" ")]
    Configurations.append(config.copy())

expectations = []
for config in Configurations:
    expectation = Simulate(ladders_=config['ladders'], snakes_=config['snakes'], probas_=config['probas']).run()
    print(expectation)
    expectations.append(expectation)
