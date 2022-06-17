import boggle_board_randomizer
import ex12_utils as ut


class Game:
    """This class represents the logical state of the game"""

    def __init__(self):
        self.timer = 180
        self.score = 0
        self.board = boggle_board_randomizer.randomize_board()
        self.words = self.read_boggle_dict()
        self.words_bank = []
        self.current_word = []
        self.game_is_over = False

    def new_board(self):
        """
        This function creates a new random board
        """
        self.board = boggle_board_randomizer.randomize_board()

    def read_boggle_dict(self):
        """
        This function reads the given word file by lines and adds every word into a set
        return: the words set
        """
        words_set = set()
        with open("boggle_dict.txt", 'r') as f:
            for word in f.readlines():
                if word != '':
                    words_set.add(word.strip())

        return words_set

    def game_over(self):
        """
        This function is activates the game_reset function when time is up
        """
        self.game_reset()

    def game_reset(self):
        """
        This function resets the game parameters to the beginning params
        """
        self.timer = 180
        self.score = 0
        self.words_bank = []
        self.current_word = []

    def get_time(self) -> str:
        """
        This function creates the game timer
        """
        return "Timer: " + str(self.timer // 60) + ":" + str(
            self.timer % 60)

    def get_score(self) -> int:
        """
        This function gets the participant's score
        """
        return self.score

    def get_forming_word(self) -> str:
        """
        This function represents the partial written word
        return: a partial word (string)
        """
        word = ""

        for x, y in self.current_word:
            word += self.board[x][y]

        return word

    def get_board(self) -> list[list[str]]:
        """
        This function returns the game board
        """
        return self.board

    def delete_letter(self):
        """
        This function activates the delete button on the game level
        """
        self.current_word = self.current_word[:len(self.current_word) - 1]

    def enter_pressed(self):
        """
        This function activates the enter button.
        if the word before pressing enter is valid- this function updates the game params,
        and if not- resets the guessed word and returns False
        """
        result = ut.is_valid_path(self.board, self.current_word, self.words)

        if not result or result in self.words_bank:
            self.reset_current_word()
            return False
        self.words_bank.append(result)
        self.score += len(self.current_word) ** 2
        self.reset_current_word()

    def get_valid_next_moves(self):
        """
        This function checks the next valid move.
        if no letter was chosen- all next letters are valid.
        if a certain letter was chosen- it returns the 8 valid letters
        """
        all_coords = {(i, j) for i in range(len(self.board)) for j in
                      range(len(self.board[0]))}
        if len(self.current_word) == 0:
            return all_coords
        else:
            return {coord for coord in all_coords if
                    ut.validate_path(self.current_word + [coord])}

    def reset_current_word(self):
        """
        This function is activated after pressing the reset button,
        it resets the current word
        """
        self.current_word = []

    def press(self, x, y):
        """
        This function is activated when pressing the letter-button
        it appends the letter to the current word rubric
        """
        self.current_word.append((x, y))
