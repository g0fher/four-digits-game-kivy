from secrets import choice

class FourDigitsGame:
    def __init__(self, length=4) -> None:
        if not 1 <= length <= 10:
            print("Bad length, defaulting to 4")
            self.length = 4
        else:
            self.length = length

        self.all_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def reset_numbers_pool(self):
        self.all_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Generate a random unique n digit number
    def generate(self) -> list:
        choice_from = self.all_numbers
        
        generated_numbers = []
        for i in range(self.length):
            generated_numbers.append(choice(choice_from))
            choice_from.remove(generated_numbers[i])

        return generated_numbers
    
    # checks if a guess numbers list has identical integers
    def check_identical(self, guess: list) -> bool:
        if len(guess) > len(set(guess)):
            print("Your number contains identical digits.")
            return True
        else:
            return False
        
    def process_guess(self, correct_numbers: list, user_guess: list) -> list:
        # first number = number of correctly guessed numbers
        # second number = number of correctly placed numbers

        answer = [0, 0]

        for i in range(self.length):
            if user_guess[i] in correct_numbers:
                answer[0] += 1
                if user_guess[i] == correct_numbers[i]:
                    answer[1] += 1
        
        return answer
