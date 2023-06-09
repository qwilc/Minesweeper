import tkinter as tk

from game import Game
from states import State
from game_modes import Mode
# import tkinter.ttk

TITLE_SIZE = 14
SUBTITLE_SIZE = 12
PAD_L = 20
PAD_M = 10
PAD_S = 5
STARTING_SUBTITLE = "Good luck"


class GUI:
    def __init__(self, game):
        self.lbl_mines_left = None
        self.lbl_time = None
        self.game = game
        self.buttons = []

    def display(self):
        window = tk.Tk()
        window.title("My Minesweeper")

        # Title
        self.lbl_title = tk.Label(
            text="Minesweeper",
            font=("Arial", TITLE_SIZE)
        )
        self.lbl_title.pack()
        # Message that updates on win/lose
        self.lbl_message = tk.Label(
            text="Good luck",
            font=("Arial", SUBTITLE_SIZE)
        )
        self.lbl_message.pack()

        # Info frame with time and number of mines left
        frm_info = tk.Frame()
        self.lbl_time = tk.Label(
            master=frm_info,
            text="Time: " + self.game.get_elapsed_time()
            )
        self.lbl_mines_left = tk.Label(master=frm_info)
        self.lbl_time.pack()
        self.lbl_mines_left.pack()
        self.update_info()
        self.update_time()
        frm_info.pack()

        # Frame for the board - grid of buttons
        self.frm_board = tk.Frame(padx=PAD_L)
        self.add_buttons()
        self.frm_board.pack()

        frm_new_game_btns = tk.Frame()
        btn_easy = tk.Button(
            master=frm_new_game_btns,
            text=str(Mode.EASY),
            command=lambda: self.restart(Mode.EASY)
        )
        btn_medium = tk.Button(
            master=frm_new_game_btns,
            text=str(Mode.MEDIUM),
            command=lambda: self.restart(Mode.MEDIUM)
        )
        btn_hard = tk.Button(
            master=frm_new_game_btns,
            text=str(Mode.HARD),
            command=lambda: self.restart(Mode.HARD)
        )

        btn_easy.grid(row=0, column=0, padx=PAD_S, pady=PAD_M)
        btn_medium.grid(row=0, column=1, padx=PAD_S, pady=PAD_M)
        btn_hard.grid(row=0, column=2, padx=PAD_S, pady=PAD_M)
        frm_new_game_btns.pack()

        window.mainloop()

    def add_buttons(self):
        self.buttons = []
        for widget in self.frm_board.winfo_children():
            widget.destroy()
        for row in range(self.game.board.height):
            for col in range(self.game.board.width):
                frame = tk.Frame(
                    master=self.frm_board
                )
                frame.grid(row=row, column=col)
                button = tk.Label(
                    master=frame,
                    width=2
                )
                self.configure_button(button, row, col)
                button.bind("<ButtonRelease-1>", lambda e, r=row, c=col: self.handle_click(e, row=r, col=c))
                button.bind("<Button-3>", lambda e, r=row, c=col: self.handle_right_click(e, row=r, col=c))
                self.buttons.append(button)
                button.pack()

    def restart(self, mode):
        self.game = Game(mode)
        self.lbl_message.configure(text=STARTING_SUBTITLE)
        self.update_info()
        self.update_time()
        self.add_buttons()

    def update(self):
        self.update_info()
        self.update_buttons()
        if self.game.is_game_over:
            self.handle_game_over()

    def update_info(self):
        self.lbl_mines_left["text"] = "Mines: " + str(self.game.num_mines_left)

    def update_time(self):
        self.lbl_time["text"] = "Time: " + self.game.get_elapsed_time()
        self.after_id = self.lbl_time.after(1000, self.update_time)

    def update_buttons(self):
        for row, col in self.game.changed_coords:
            idx = row * self.game.board.width + col
            button = self.buttons[idx]
            self.configure_button(button, row, col)
        self.game.changed_coords = []

    def handle_game_over(self):
        self.lbl_time.after_cancel(self.after_id)
        self.lbl_message["text"] = self.game.final_message
        for idx, frm in enumerate(self.frm_board.children.values()):
            for btn in frm.children.values():
                btn["state"] = tk.DISABLED
                btn.unbind("<ButtonRelease-1>")
                btn.unbind("<Button-3>")
                row_idx = idx // self.game.board.width
                col_idx = idx % self.game.board.width
                btn["text"] = self.get_btn_text(row_idx, col_idx)

    def handle_click(self, event, row, col):
        if not self.game.is_started:
            self.game.start(row, col)
        button = event.widget
        self.game.is_action_dig = True
        self.game.perform_action_on(row, col)
        self.update()

    def handle_right_click(self, event, row, col):
        button = event.widget
        self.game.is_action_dig = False
        self.game.perform_action_on(row, col)
        self.update()

    def configure_button(self, button, row, col):
        state = self.game.board[row][col].state
        if state == State.HIDDEN or state == State.FLAGGED:
            relief = tk.RAISED
        else:
            relief = tk.GROOVE

        button.configure(
            text=self.get_btn_text(row, col),
            relief=relief
        )

    def get_btn_text(self, row, col):
        return str(self.game.board[row][col])
