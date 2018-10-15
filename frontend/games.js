'use strict';
import React from "react";
import {render} from "react-dom";
import Puzzle from "./games/Puzzle";
import Quiz from "./games/Quiz";


let puzzle = document.getElementById('puzzle');
if (puzzle !== null) {
    render(<Puzzle />, puzzle);
}


let quiz = document.getElementById('quiz');
if (quiz !== null) {
    render(<Quiz />, quiz);
}
