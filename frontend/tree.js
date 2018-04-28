import React from "react";
import {render} from "react-dom";
import Map from './components/Map';
import Tree from "./components/Tree";
import {decodePolygon} from "./utils";


class RegionTree extends React.Component {
    constructor(props) {
        super(props);
        let polygons = window.__CHECKED__.map((polygon) => {
            polygon.id = polygon.id.toString();
            polygon.paths = decodePolygon(polygon.paths);
            polygon.isSolved = true;
            polygon.draggable = false;
            return polygon;
        });
        this.state = {regions: polygons, items: window.__REGIONS__,
            checked: new Set(window.__CHECKED__.reduce(
                (acc, item) => {
                    acc.push(item.id);
                    return acc;
                }, []))}
    }

    static convertRegion(obj) {
        return {
            id: obj.id.toString(),
            isSolved: true,
            draggable: false,
            name: obj.infobox.name,
            paths: decodePolygon(obj.polygon),
        };
    }

    onChange = (event) => {
        let checked = this.state.checked;
        let value = event.target.value;
        if (checked.has(value)) {
            checked.delete(value);
            this.setState({...this.state, checked: checked, regions: this.state.regions.filter(obj => obj.id !== value)});
        } else {
            fetch(`/regions/${value}/`, ).then(response => {
                response.json().then(obj => {
                    checked.add(value);
                    let regions = this.state.regions;
                    regions.push(RegionTree.convertRegion(obj));
                    this.setState({...this.state, checked: checked, regions: regions});
                });
            });
        }
    };

    static attachItems(regions, id, items) {
        regions.map(region => {
            if (region.id === id) {
                region.items = items;
                region.toggled = true;
            }
            if (region.items && region.items.length > 0) {
                region.items = RegionTree.attachItems(region.items, id, items);
            }
            return region;
        });
        return regions;
    }

    loadItems = (id) => {
        fetch(`/regions/${id}/items/`).then(response => {
            response.json().then(items => {
                let regions = RegionTree.attachItems(this.state.items, id, items);
                this.setState({...this.state, items: regions});
            });
        });
    };


    render() {
        return <div>
            <Tree {...this.state} onChange={this.onChange} loadItems={this.loadItems}/>
            <Map regions={this.state.regions} mapTypeId="terrain"/>
            <p>Position and zoom will be saved as default for that game.</p>
        </div>;
    }
}


render(<RegionTree />, document.getElementById('tree'));
