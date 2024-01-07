import React from "react";
import GoogleMap from "./GoogleMap";


class Map extends React.Component {
  static moveTo(path, from, to) {
    return GoogleMap.moveTo(path, from, to);
  }

  static preparePolygon(polygon, useDecode) {
    return GoogleMap.preparePolygon(polygon, useDecode);
  }

  render() {
    return <GoogleMap {...this.props}/>;
  }
}

export default Map;