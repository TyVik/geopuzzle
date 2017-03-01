import React from "react";
import Map from '../Map';
import Loading from '../Loading';
import Infobox from '../Infobox';
import Toolbox from '../Toolbox';
import Congratulation from '../Congratulation';


const Puzzle = () => {
    return (
        <div>
            <Loading/>
            <Map/>
            <Infobox/>
            <Toolbox/>
            <Congratulation/>
        </div>
    )
};

export default Puzzle
