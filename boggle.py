from tkinter import *
from tkinter import messagebox

# from tkinter.ttk import *
# from PIL import Image, ImageTk
import game

"""Magic Variables:"""
BUTTON_HOVER_COLOR = 'light blue'
REGULAR_COLOR_FOR_TOP_FRAME = 'green'
REGULAR_COLOR = 'grey'
BUTTON_ACTIVE_COLOR = 'blue'
TIMER_COLOR = 'white'
ENTER_COLOR = 'yellow'
LIST_OF_GUESS_COLOR = 'black'
DEL_BUTTON_COLOR = 'red'
RESET_BUTTON_COLOR = 'green'

BUTTON_STYLE = {"font": ("David", 40),
                "borderwidth": 3,
                "relief": RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR,
                "width": 3,
                "height": 1}


class Screen:
    """
    this class is the class that creates the screen object.
    """

    def __init__(self):
        self.game_obj = game.Game()
        self.root = Tk()
        self.root.title("Noam & Daphi's game!")
        self.root.resizable(False, False)
        self.start_frame = Frame(self.root)
        self.main_frame = Frame(self.root)
        self.game_over_frame = Frame(self.root)
        self.restart_frame = Frame(self.root)
        self.score = IntVar()
        self.time = StringVar()
        self.word = StringVar()
        self.buttons = dict()
        self.words_bank = None
        self.update_vars()
        self.init_frames()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """
        this method is a double-checking if the player wants to quit the game.
        :return: None.
        """
        msg = "are you sure you want to quit?"
        answer = messagebox.askyesno(title="quit", message=msg)
        if answer:
            self.root.destroy()
        else:
            pass

    def update_vars(self):
        """
        this method updates the screen parameters
        :return: None
        """
        self.score.set(self.game_obj.get_score())
        self.word.set(self.game_obj.get_forming_word())
        valid_next_moves = self.game_obj.get_valid_next_moves()
        for coord in self.buttons:
            if coord in valid_next_moves:
                self.buttons[coord]["state"] = "normal"
            else:
                self.buttons[coord]["state"] = "disabled"

        if self.words_bank:
            self.words_bank.delete(1, END)
            for word in self.game_obj.words_bank:
                self.words_bank.insert(END, word)

    def update_time(self):
        """
        this method updates the time value.
        :return: None
        """
        if self.game_obj.timer == 0:
            self.main_frame.grid_forget()
            self.init_game_over_frame()
            self.game_obj.game_over()
            return

        self.time.set(self.game_obj.get_time())
        self.game_obj.timer -= 1

        self.root.after(1000, self.update_time)

    def init_frames(self):
        """
        this method is creating the two main frames for the game display.
        :return: None
        """
        self.init_start_frame()
        self.init_main_frame()

    def init_game_over_frame(self):
        """
        this method creates the scenario when the game needs to be over.
        :return: None
        """
        img = PhotoImage(file="game_over.png")
        panel = Label(self.game_over_frame, image=img)
        panel.photo = img
        panel.grid(row=0)

        game_over_button = Button(self.game_over_frame, text="RESTART",
                                  font="David 16 bold", bg=TIMER_COLOR,
                                  command=self.restart_command, width=30)
        game_over_button.grid(row=1, pady=3)

        self.game_over_frame.grid()

    def init_start_frame(self):
        """
        this method is the creation of the start frame.
        :return: None.
        """
        img = PhotoImage(file="boggle.png")
        panel = Label(self.start_frame, image=img)
        panel.photo = img
        panel.grid(row=0)

        start_button = Button(self.start_frame, text="Start Game!",
                              font="David 16 bold", bg=TIMER_COLOR,
                              command=self.start_command, width=30)
        start_button.grid(row=1, pady=3)

        self.start_frame.grid()

    def init_main_frame(self):
        """
        this method initializes the main frame.
        :return: None
        """
        self.init_top_frame()
        self.init_board_frame()
        self.init_found_words()
        pass

    def init_top_frame(self):
        """
        this method initializes the top frame for the main frame.
        :return:None.
        """
        top_frame = Frame(self.main_frame, bg=REGULAR_COLOR_FOR_TOP_FRAME,
                          highlightbackground=REGULAR_COLOR_FOR_TOP_FRAME,
                          highlightthickness=4)

        score_label = Label(top_frame, textvariable=self.score,
                            font="David 14", highlightthickness=4)
        word_label = Label(top_frame, textvariable=self.word, font="David 14 ",
                           highlightthickness=4)
        time_label = Label(top_frame, textvariable=self.time, font="David 14 ",
                           highlightthickness=4)

        word_label.pack(side=LEFT, fill=X, expand=True, padx=5)
        score_label.pack(side=LEFT, padx=5)
        time_label.pack(side=RIGHT, padx=5)

        top_frame.grid(row=0, columnspan=2, sticky=EW)
        return

    def init_board_frame(self):
        """
        this method initializes the board frame for the main frame.
        :return: None
        """

        board_frame = Frame(self.main_frame)
        game_board = self.game_obj.get_board()

        for i in range(len(game_board)):
            for j in range(len(game_board[i])):
                self.create_button(i, j, game_board[i][j], board_frame)
        board_frame.grid(row=1, column=0)

    def create_button(self, i, j, char, board_frame):
        """
        this method is creating the buttons for the game board.
        :param i: x coordinate.
        :param j: y coordinate.
        :param char: the val of one box in the game board.
        :param board_frame: the frame of the game board.
        :return: None.
        """

        def _on_enter(event):
            button['background'] = BUTTON_HOVER_COLOR

        def _on_leave(event):
            button['background'] = REGULAR_COLOR

        button = Button(board_frame,
                        text=char,
                        command=lambda: self.press(i, j),
                        **BUTTON_STYLE)

        self.buttons[(i, j)] = button

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        button.grid(row=i, column=j)
        return

    def press(self, i, j):
        """
        This method is activated when the user pressed one of the letter button.
        :param i: x coordinate.
        :param j: y coordinate.
        """
        result = self.game_obj.press(i, j)
        self.update_vars()

    def init_found_words(self):
        """
        this method initializes the second section for the frame
        for the main frame.
        :return: None.
        """
        words_frame = Frame(self.main_frame, borderwidth=5, relief="ridge")
        self.words_bank = Listbox(words_frame, fg='black',
                                  bg=ENTER_COLOR,
                                  font="David, 20 bold")
        self.words_bank.insert(END, "Words Bank")

        BUTTON_ENTER = Button(words_frame, text='Enter',
                              fg='black', bg=ENTER_COLOR,
                              font="David, 20 bold",
                              activebackground=BUTTON_ACTIVE_COLOR,
                              command=self.enter_button)

        BUTTON_RESET = Button(words_frame, text='Reset',
                              fg='black', bg=RESET_BUTTON_COLOR,
                              font="David, 20 bold",
                              activebackground=BUTTON_ACTIVE_COLOR,
                              command=self.reset_button)

        BUTTON_DEL = Button(words_frame, text='del',
                            fg='black', bg=DEL_BUTTON_COLOR,
                            font="David, 20 bold",
                            activebackground=BUTTON_ACTIVE_COLOR,
                            command=self.del_button)

        self.words_bank.pack(side=TOP, expand=True, fill=Y, pady=60)
        BUTTON_RESET.pack(side=RIGHT, pady=5)
        BUTTON_DEL.pack(side=LEFT, pady=5)
        BUTTON_ENTER.pack(side=TOP, pady=10)
        words_frame.grid(row=1, column=1, sticky=NSEW)

    def reset_button(self):
        """
        this method resets the current forming word.
        :return: None
        """
        self.word.set("")
        self.game_obj.reset_current_word()
        self.update_vars()

    def del_button(self):
        """
        this method deletes a letter.
        :return: None
        """
        self.game_obj.delete_letter()
        self.update_vars()

    def enter_button(self):
        """
        this method is operating the enter button a button.
        :return: None
        """
        self.game_obj.enter_pressed()
        self.word.set("")
        self.update_vars()

    def start_command(self):
        """
        this method is initializing the grid command for the two main frames.
        :return: None.
        """
        self.start_frame.grid_forget()
        self.main_frame.grid()
        self.update_time()
        self.update_vars()

    def restart_command(self):
        """
        this method is resetting the game itself.
        :return: None
        """
        self.game_obj = game.Game()
        self.game_over_frame.grid_forget()
        self.game_obj.new_board()

        for key, value in self.buttons.items():
            value.config(text=self.game_obj.get_board()[key[0]][key[1]])

        self.start_frame.grid()
        self.update_vars()

    def run(self):
        """
        this func is running the game.
        :return: None.
        """
        self.root.mainloop()


################################not_ready##################################

###########################################################################

if __name__ == "__main__":
    cg = Screen()
    cg.run()
