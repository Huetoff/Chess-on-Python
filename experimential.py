import chess
import chess.svg
from tkinter import *
from tkinter import messagebox  # Импортируем messagebox для отображения сообщений
from PIL import Image, ImageTk
import io

class ChessGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Шахматы")

        self.board = chess.Board()
        self.selected_square = None  # Инициализируем переменную для хранения выбранной клетки
        self.canvas = Canvas(master, width=480, height=480)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)
        self.update_board()

    def update_board(self):
        self.canvas.delete("all")  # Очищаем канвас перед обновлением
        square_size = 60  # Размер каждой клетки доски
        self.images = []  # Список для хранения ссылок на изображения

        for row in range(8):
            for col in range(8):
                square_color = "white" if (row + col) % 2 == 0 else "gray"
                self.canvas.create_rectangle(col * square_size, row * square_size,
                                             (col + 1) * square_size, (row + 1) * square_size,
                                             fill=square_color)

                piece = self.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_color = 'w' if piece.color else 'b'
                    piece_type = piece.piece_type
                    piece_image_path = f'images/{piece_color}_{piece_type}.png'
                
                    # Открываем и изменяем размер изображения только если фигура есть
                    piece_image = Image.open(piece_image_path)
                    piece_image = piece_image.resize((square_size, square_size), Image.LANCZOS)
                    piece_photo = ImageTk.PhotoImage(piece_image)

                    # Сохраняем ссылку на изображение в списке
                    self.images.append(piece_photo)
                    self.canvas.create_image(col * square_size, row * square_size, anchor=NW, image=piece_photo)

        # Сохраняем ссылки на все изображения, чтобы они не были собраны сборщиком мусора
        self.canvas.images = self.images

    def on_click(self, event):
        square_size = 60  # Размер каждой клетки доски
        row = event.y // square_size
        col = event.x // square_size
        square = chess.square(col, 7 - row)  # Система координат Tkinter зеркальная

        if self.selected_square is None:  # Если фигура еще не выбрана
            if self.board.piece_at(square) is not None and self.board.turn == self.board.piece_at(square).color:
                self.selected_square = square
                print(f"Выбрано: {chess.square_name(square)}")
        else:  # Если фигура уже выбрана
            move = chess.Move(self.selected_square, square)

            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None  # Сбрасываем выбранную клетку
                self.update_board()
                if self.board.is_checkmate():
                    winner = 'Черные' if self.board.turn else 'Белые'
                    messagebox.showinfo("Мат!", f"{winner} выиграли!")
                    self.reset_game()
            else:
                print("Неверный ход. Попробуйте снова.")
                self.selected_square = None  # Сбрасываем выбранную клетку

    def reset_game(self):
        self.board = chess.Board()
        self.selected_square = None  # Сбрасываем выбранную клетку
        self.update_board()

if __name__ == "__main__":
    root = Tk()
    game = ChessGame(root)
    root.mainloop()
