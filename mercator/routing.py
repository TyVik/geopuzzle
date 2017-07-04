from puzzle.consumer import routes as puzzle_routes
from quiz.consumer import routes as quiz_routes


channels = puzzle_routes + quiz_routes
