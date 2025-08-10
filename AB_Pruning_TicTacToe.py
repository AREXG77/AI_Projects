import tkinter as tk
from tkinter import messagebox
import copy

# Constants
PLAYER = 'X'
AI = 'O'
EMPTY = ' '

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - AI Game")
        self.buttons = [[None]*3 for _ in range(3)]
        self.board = [[EMPTY]*3 for _ in range(3)]
        self.create_buttons()
        self.player_turn = True  # Player starts first
    
    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text=' ', font=('Arial', 40), width=5, height=2,
                                command=lambda r=i, c=j: self.player_move(r,c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def player_move(self, row, col):
        if self.player_turn and self.board[row][col] == EMPTY:
            self.make_move(row, col, PLAYER)
            if self.check_winner(self.board, PLAYER):
                self.end_game("You Win!")
            elif self.is_draw(self.board):
                self.end_game("Draw!")
            else:
                self.player_turn = False
                self.root.after(500, self.ai_move)  # Let AI play after delay

    def ai_move(self):
        move = self.best_move(self.board)
        if move:
            self.make_move(move[0], move[1], AI)
            if self.check_winner(self.board, AI):
                self.end_game("AI Wins!")
            elif self.is_draw(self.board):
                self.end_game("Draw!")
            else:
                self.player_turn = True

    def make_move(self, row, col, player):
        self.board[row][col] = player
        self.buttons[row][col].config(text=player, state=tk.DISABLED)

    def check_winner(self, board, player):
        # Check rows, cols, diagonals
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
            if all(board[j][i] == player for j in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_draw(self, board):
        return all(board[i][j] != EMPTY for i in range(3) for j in range(3))

    def best_move(self, board):
        best_score = float('-inf')
        move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    score = self.minimax(board, 0, False)
                    board[i][j] = EMPTY
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner(board, AI):
            return 10 - depth
        elif self.check_winner(board, PLAYER):
            return depth - 10
        elif self.is_draw(board):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = AI
                        score = self.minimax(board, depth+1, False)
                        board[i][j] = EMPTY
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER
                        score = self.minimax(board, depth+1, True)
                        board[i][j] = EMPTY
                        best_score = min(score, best_score)
            return best_score

    def end_game(self, result):
        messagebox.showinfo("Game Over", result)
        self.reset_game()

    def reset_game(self):
        self.board = [[EMPTY]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ', state=tk.NORMAL)
        self.player_turn = True

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
