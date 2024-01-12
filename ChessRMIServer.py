import Pyro4
import chess

@Pyro4.expose
class ChessRMIServer:
    def __init__(self):
        self.board = chess.Board()
        self.current_player = "White"  # Mulai dengan pemain putih

    def get_board(self):
        return self.board.fen()

    def get_current_player(self):
        return self.current_player

    def make_move(self, move_uci):
        move = chess.Move.from_uci(move_uci)
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        else:
            return False

    def switch_player(self):
        self.current_player = "Black" if self.current_player == "White" else "White"

    def check_game_status(self):
        if self.board.is_checkmate():
            return f"Checkmate! {self.current_player} wins!"
        elif self.board.is_stalemate():
            return "Stalemate! The game is a draw."
        elif self.board.is_insufficient_material():
            return "Insufficient material! The game is a draw."
        elif self.board.is_seventyfive_moves():
            return "The game is a draw (75-move rule)."
        elif self.board.is_fivefold_repetition():
            return "The game is a draw (fivefold repetition)."
        else:
            return None  # Permainan masih berlanjut

if __name__ == "__main__":
    daemon = Pyro4.Daemon()
    uri = daemon.register(ChessRMIServer)
    ns = Pyro4.locateNS()
    ns.register("ChessRMIServer", uri)

    print("Chess RMI Server is ready. Object uri =", uri)
    daemon.requestLoop()
