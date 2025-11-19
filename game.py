from typing import List, Optional, Tuple
from enum import Enum
import json

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
        if self.status != GameStatus.IN_PROGRESS:
            return {"success": False, "error": "Game is over"}
        
        if col < 0 or col >= self.cols:
            return {"success": False, "error": "Invalid column"}
        
        row = self._find_available_row(col)
        if row is None:
            return {"success": False, "error": "Column is full"}
        
        self.board[row][col] = self.current_player
        self.move_count += 1
        
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
        
        if self.move_count == self.rows * self.cols:
            self.status = GameStatus.DRAW
            return {
                "success": True,
                "row": row,
                "col": col,
                "player": self.current_player.name,
                "status": self.status.value
            }
        
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
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == Player.EMPTY:
                return row
        return None
    
    def _check_win(self, row: int, col: int) -> bool:
        player = self.board[row][col]
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            positions = [(row, col)]
            
            r, c = row + dr, col + dc
            while (0 <= r < self.rows and 0 <= c < self.cols and 
                   self.board[r][c] == player):
                positions.append((r, c))
                r += dr
                c += dc
            
            r, c = row - dr, col - dc
            while (0 <= r < self.rows and 0 <= c < self.cols and 
                   self.board[r][c] == player):
                positions.append((r, c))
                r -= dr
                c -= dc
            
            if len(positions) >= 4:
                self.winning_positions = positions
                return True
        
        return False
    
    def get_board(self) -> List[List[str]]:
        return [[cell.name for cell in row] for row in self.board]
    
    def get_valid_moves(self) -> List[int]:
        return [col for col in range(self.cols) 
                if self.board[0][col] == Player.EMPTY]
    
    def reset(self):
        self.board = [[Player.EMPTY] * self.cols for _ in range(self.rows)]
        self.current_player = Player.RED
        self.move_count = 0
        self.status = GameStatus.IN_PROGRESS
        self.winning_positions = []
    
    def get_game_state(self) -> dict:
        return {
            "board": self.get_board(),
            "current_player": self.current_player.name,
            "status": self.status.value,
            "valid_moves": self.get_valid_moves(),
            "move_count": self.move_count,
            "winning_positions": self.winning_positions
        }
