from flask import Flask, request, render_template,jsonify
app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

import chess
import chess.svg

from flask import Markup

starter = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1' #change this whenever you want the board to change

#function to make the board
def makeBoard(FEN = starter):
    board = chess.Board(FEN)
    svg = chess.svg.board(board, size=350) #make the svg
    return svg

#display homepage
@app.route('/')
def home(FEN = starter):
    svg = makeBoard(FEN)
    #display svg
    #https://stackoverflow.com/questions/50851054/how-can-i-load-svg-file-into-my-python-flask-page
    return render_template('index.html', svg=Markup(svg))

#run python script with button onclick
#https://github.com/hackanons/button-python-click/tree/master/Run%20Python%20Script%20Html%20Flask/Html%20Button%20to%20Python%20Script
@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]


    return render_template('index.html', name = name)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080) # This line is required to run Flask on repl.it