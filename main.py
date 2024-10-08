from flask import Flask, request, render_template,jsonify
app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

import chess
import chess.svg

from flask import Markup

starter = 'rnbqkbnr/8/8/PPPPPPPP/PPPPPPPP/8/8/3qk3 w KQkq - 0 1' #change this whenever you want the board to change
board = chess.Board(starter)
#function to make the board
def makeBoard(FEN = starter):
    board = chess.Board(FEN)
    svg = chess.svg.board(board, size=350) #make the svg
    return svg

#display homepage
@app.route('/')
def home(board = chess.Board(starter)):
    #svg = makeBoard(FEN)
    svg = chess.svg.board(board, size=350) #make the svg
    #display svg
    #https://stackoverflow.com/questions/50851054/how-can-i-load-svg-file-into-my-python-flask-page
    return render_template('index.html', svg=Markup(svg), turn="white", status="")

#function that allows a human player to make a move
def human(board, moveInput):
    #displayBoard(board) #display the board after every turn
    #moveInput = input("make a legal move: ")
    if moveInput=="":
        print("need to input valid move")
        return board
    move = chess.Move.from_uci(moveInput) #make the move
    if move in board.legal_moves: #if the move is legal
        board.push(move) #push the move
    elif chess.Move.from_uci(moveInput + "q") in board.legal_moves: #check if promotion
        moveInput+='q' #autopromote to queen
        #moveInput += input("Which piece you want to promote the pawn to? [q,r,b,n]: ") #promotion query
        move = chess.Move.from_uci(moveInput) #make the move
        board.push(move) #push the move
    else:
        print("invalid move. try again")
    return board

#function to check whose turn it is
def getTurn(board):
    #True = white, False = black
    if(board.turn):
        return("white")
    return("black")

#function to check the status of the game
def getStatus(board):
    status = "" #default status
    #Verifying check
    if(board.is_check()):
        status = "check"
    #Verifying checkmate
    if(board.is_checkmate()):
        status = "checkmate"

    #Verifying stalemate
    if(board.is_stalemate()):
        status = "stalemate"
    
    return status

#run python script with button onclick
#https://github.com/hackanons/button-python-click/tree/master/Run%20Python%20Script%20Html%20Flask/Html%20Button%20to%20Python%20Script
@app.route('/',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"] #move the user inputted
    global board #make the board a global variable
    board = human(board, name)
    #home(board)
    svg = chess.svg.board(board, size=350) #make the svg
    turn = getTurn(board)
    status = getStatus(board)
    return render_template('index.html', svg=Markup(svg), turn=turn, status=status)


    #return render_template('index.html', name = name)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080) # This line is required to run Flask on repl.it