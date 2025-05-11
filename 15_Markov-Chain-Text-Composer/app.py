'''
This is a simple Markov chain text generator that can be used to generate text based on a given input text.
'''

import random

class MarkovTextComposer:
    def __init__(self, order=1):
        self.order = order
        self.markov_chain = {}

    def train(self, text):
        tokens = text.split()
        
        for i in range(len(tokens) - self.order):
            current_state = tuple(tokens[i:i+self.order])
            next_state = tokens[i+self.order]

            if current_state not in self.markov_chain:
                self.markov_chain[current_state] = {}

            if next_state not in self.markov_chain[current_state]:
                self.markov_chain[current_state][next_state] = 0

            self.markov_chain[current_state][next_state] += 1

    def generate_text(self, length):
        current_state = random.choice(list(self.markov_chain.keys()))
        generated_text = list(current_state)

        for _ in range(length - self.order):
            if current_state in self.markov_chain:
                next_state = random.choices(
                    list(self.markov_chain[current_state].keys()),
                    list(self.markov_chain[current_state].values())
                )[0]
                generated_text.append(next_state)
                current_state = tuple(generated_text[-self.order:])
            else:
                break

        return ' '.join(generated_text)

# Example usage "You can write your own example here also":
lyrics = """
    I'm a little teapot
    Short and stout
    Here is my handle
    Here is my spout
    When I get all steamed up
    Hear me shout
    Tip me over and pour me out
"""

composer = MarkovTextComposer(order=2)
composer.train(lyrics)

generated_lyrics = composer.generate_text(length=20)
print(generated_lyrics)

#by default it will generate 20 words of text based on the trained lyrics.
# You can change the length parameter in the generate_text method to get more or less text.