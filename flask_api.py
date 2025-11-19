from flask import Flask, render_template_string, jsonify, request
from game import Connect4, Player, GameStatus


app = Flask(__name__)
game = Connect4()

@app.route('/')
def index():
    # Read the HTML template from game.html
    with open('game.html', 'r') as file:
        html_content = file.read()
    return render_template_string(html_content)

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(game.get_game_state())

@app.route('/api/move', methods=['POST'])
def make_move():
    data = request.get_json()
    col = data.get('column')
    
    if col is None:
        return jsonify({"success": False, "error": "Column not specified"}), 400
    
    result = game.drop_piece(col)
    return jsonify(result)

@app.route('/api/reset', methods=['POST'])
def reset_game():
    game.reset()
    return jsonify({"success": True, "message": "Game reset"})


if __name__ == '__main__':
    print("🎮 Connect 4 Game Server Starting...")
    print("📍 Open http://localhost:5000 in your browser")
    print("👥 Two players can play on the same device!")
    app.run(debug=True, host='0.0.0.0', port=5000)