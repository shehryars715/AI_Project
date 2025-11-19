from typing import List, Optional, Tuple
from enum import Enum

class Player(Enum):
    EMPTY = 0
    RED = 1
    YELLOW = 2

class GameStatus(Enum):
    IN_PROGRESS = "in_progress"
    RED_WINS = "red_wins"
    YELLOW_WINS = "yellow_wins"
    DRAW = "draw"

class Connect4:
    def __init__(self, rows: int = 6, cols: int = 7):
        self.rows = rows
        self.cols = cols
        self.board: List[List[Player]] = [[Player.EMPTY] * cols for _ in range(rows)]
        self.current_player = Player.RED
        self.move_count = 0
        self.status = GameStatus.IN_PROGRESS
        self.winning_positions: List[Tuple[int, int]] = []
    
    def drop_piece(self, col: int) -> dict:
        """Drop a piece in the specified column. Returns result of the move."""
        if self.status != GameStatus.IN_PROGRESS:
            return {"success": False, "error": "Game is over"}
        
        if col < 0 or col >= self.cols:
            return {"success": False, "error": "Invalid column"}
        
        # Find the lowest empty row in this column
        row = self._find_available_row(col)
        if row is None:
            return {"success": False, "error": "Column is full"}
        
        # Place the piece
        self.board[row][col] = self.current_player
        self.move_count += 1
        
        # Check for win
        if self._check_win(row, col):
            self.status = (GameStatus.RED_WINS if self.current_player == Player.RED 
                          else GameStatus.YELLOW_WINS)
            return {
                "success": True,
                "row": row,
                "col": col,
                "player": self.current_player.name,
                "status": self.status.value,
                "winning_positions": self.winning_positions
            }
        
        # Check for draw
        if self.move_count == self.rows * self.cols:
            self.status = GameStatus.DRAW
            return {
                "success": True,
                "row": row,
                "col": col,
                "player": self.current_player.name,
                "status": self.status.value
            }
        
        # Switch player
        self.current_player = (Player.YELLOW if self.current_player == Player.RED 
                              else Player.RED)
        
        return {
            "success": True,
            "row": row,
            "col": col,
            "player": Player.RED.name if self.current_player == Player.YELLOW else Player.YELLOW.name,
            "status": self.status.value,
            "next_player": self.current_player.name
        }
    
    def _find_available_row(self, col: int) -> Optional[int]:
        """Find the lowest empty row in a column."""
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == Player.EMPTY:
                return row
        return None
    
    def _check_win(self, row: int, col: int) -> bool:
        """Check if the last move resulted in a win."""
        player = self.board[row][col]
        
        # Check all four directions: horizontal, vertical, diagonal, anti-diagonal
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal
            (1, -1)   # Anti-diagonal
        ]
        
        for dr, dc in directions:
            positions = [(row, col)]
            
            # Check positive direction
            r, c = row + dr, col + dc
            while (0 <= r < self.rows and 0 <= c < self.cols and 
                   self.board[r][c] == player):
                positions.append((r, c))
                r += dr
                c += dc
            
            # Check negative direction
            r, c = row - dr, col - dc
            while (0 <= r < self.rows and 0 <= c < self.cols and 
                   self.board[r][c] == player):
                positions.append((r, c))
                r -= dr
                c -= dc
            
            # Check if we have 4 in a row
            if len(positions) >= 4:
                self.winning_positions = positions
                return True
        
        return False
    
    def get_board(self) -> List[List[str]]:
        """Return the board as a 2D list of strings."""
        return [[cell.name for cell in row] for row in self.board]
    
    def get_valid_moves(self) -> List[int]:
        """Return list of columns that aren't full."""
        return [col for col in range(self.cols) 
                if self.board[0][col] == Player.EMPTY]
    
    def reset(self):
        """Reset the game to initial state."""
        self.board = [[Player.EMPTY] * self.cols for _ in range(self.rows)]
        self.current_player = Player.RED
        self.move_count = 0
        self.status = GameStatus.IN_PROGRESS
        self.winning_positions = []
    
    def get_game_state(self) -> dict:
        """Get complete game state."""
        return {
            "board": self.get_board(),
            "current_player": self.current_player.name,
            "status": self.status.value,
            "valid_moves": self.get_valid_moves(),
            "move_count": self.move_count,
            "winning_positions": self.winning_positions
        }


# Example usage
if __name__ == "__main__":
    game = Connect4()
    
    # Simulate a game
    moves = [3, 3, 4, 4, 5, 5, 6]  # Red wins diagonally
    
    for move in moves:
        result = game.drop_piece(move)
        print(f"\nMove: Column {move}")
        print(f"Result: {result}")
        
        # Print board
        print("\nCurrent board:")
        for row in game.get_board():
            print(" ".join(f"{cell:7}" for cell in row))
        
        if result.get("status") != "in_progress":
            print(f"\nGame Over! Status: {result['status']}")
            break
    
    print(f"\nFinal game state: {game.get_game_state()}")