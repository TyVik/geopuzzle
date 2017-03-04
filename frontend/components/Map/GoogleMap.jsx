import React from "react";

import {GoogleMap, withGoogleMap} from "react-google-maps";
import Polygon from "../Polygon";


export default withGoogleMap(props => {
    return <GoogleMap
        ref={props.onMapLoad}
        defaultZoom={props.zoom}
        defaultCenter={props.center}
        mapTypeId={props.mapTypeId}
        options={props.options}
    >
        {props.polygons.map(polygon => (
            <Polygon key={polygon.options.id} {...polygon} />
        ))}
    </GoogleMap>
});
