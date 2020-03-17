import random
secretNumber = random.randint(1, 20)
print('Please enter a number between 1 and 20')

for guessTaken in range(1, 7):
    print('Guess: ')
    guess = int(input())

    if guess < secretNumber:
        print('Guess too low')
    elif guess > secretNumber:
        print('Guess too high')
    else: break
if guess == secretNumber:
    print('Correct, you took ' + str(guessTaken) + ' tries!')
else:
    print('You lose, the answer is ' + str(secretNumber) + '!')