'use strict';
import React from "react";
import {render} from "react-dom";
import Workshop from "./workshop/index";


let node = document.getElementById('workshop');

render(<Workshop count={parseInt(node.dataset.count, 10)}/>, node);
