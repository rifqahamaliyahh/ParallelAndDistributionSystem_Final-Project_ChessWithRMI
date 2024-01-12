import Pyro4
import chess

# Custom piece symbols
piece_symbols = {
    "R": "♖", "r": "♜",
    "N": "♘", "n": "♞",
    "B": "♗", "b": "♝",
    "Q": "♕", "q": "♛",
    "K": "♔", "k": "♚",
    "P": "♙", "p": "♟",
}

def print_chessboard(board_fen):
    board = chess.Board(board_fen)
    print("")
    for rank in range(7, -1, -1):  # Iterate from rank 8 to rank 1
        #print(" +----+----+----+----+----+----+----+----+")
        if rank == 7:
            print("     a       b       c       d       e       f       g       h")
            print("  ╔══════╦═══════╦═══════╦═══════╦═══════╦═══════╦═══════╦═══════╗ ")
        else:
        	print("  ╠══════╬═══════╬═══════╬═══════╬═══════╬═══════╬═══════╬═══════╣ ")
        print(f"{rank + 1} ║", end=" ")  # Print rank number

        for file in range(8):
            piece = board.piece_at(chess.square(file, rank))
            piece_symbol = piece_symbols[piece.symbol()] if piece else " "
            print(f" {piece_symbol}   ║ ", end=" ")

        print()  # Move to the next line

    print("  ╚══════╩═══════╩═══════╩═══════╩═══════╩═══════╩═══════╩═══════╝ ")
    print("     a       b       c       d       e       f       g       h")
    print("")





if __name__ == "__main__":
    uri = "PYRONAME:ChessRMIServer@localhost:9090"
    chess_server = Pyro4.Proxy(uri)

    print("Welcome to Chess Game!")

    while True:
        print(f"\nCurrent player: {chess_server.get_current_player()}")
        print_chessboard(chess_server.get_board())

        move_uci = input("Enter your move (in UCI format, e.g., 'e2e4'): ")
        if chess_server.make_move(move_uci):
            print("Move successful!")
            result = chess_server.check_game_status()
            if result:
                print_chessboard(chess_server.get_board())
                print(result)
                break  # Exit the loop if the game is over
            chess_server.switch_player()
        else:
            print("Invalid move. Try again.")
