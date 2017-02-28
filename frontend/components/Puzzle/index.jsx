import React from "react";
import Map from '../Map';
import Loading from '../Loading';
import Infobox from '../Infobox';


const Puzzle = () => {
    return (
        <div>
            <Loading/>
            <Map/>
            <Infobox/>
        </div>
    )
};

export default Puzzle
