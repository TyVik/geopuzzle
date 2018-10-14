'use strict';
import React from "react";
import {render} from "react-dom";
import Workshop from "./components/Workshop";


let node = document.getElementById('workshop');

render(<Workshop count={parseInt(node.dataset.count, 10)}/>, node);
