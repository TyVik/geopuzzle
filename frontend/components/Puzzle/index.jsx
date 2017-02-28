import React from "react";
import Map from '../Map';
import Loading from '../Loading';
import Infobox from '../Infobox';
import Toolbox from '../Toolbox';


const Puzzle = () => {
    return (
        <div>
            <Loading/>
            <Map/>
            <Infobox/>
            <Toolbox/>
        </div>
    )
};

export default Puzzle
