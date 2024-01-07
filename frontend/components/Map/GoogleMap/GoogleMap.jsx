'use strict';
import React from "react";

import {GoogleMap, withGoogleMap, Marker} from "react-google-maps";
import Region from "./Region";


export default withGoogleMap(props => {
  return <GoogleMap
    ref={props.onMapLoad}
    defaultZoom={props.map.zoom}
    defaultCenter={props.map.center}
    mapTypeId={props.mapTypeId}
    options={props.map.options}
    onClick={props.onMapClick}
  >
    <Marker {...props.marker}/>
    {props.regions.map(polygon => (
      <Region key={polygon.key} {...polygon} />
    ))}
  </GoogleMap>;
});
