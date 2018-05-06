import React from "react";
import {render} from "react-dom";
import Map from './components/Map';
import Tree from "./components/Tree";
import {decodePolygon, CSRFfetch} from "./utils";
import html2canvas from 'html2canvas';


class Editor extends React.Component {
    constructor(props) {
        super(props);
        let polygons = window.__CHECKED__.map((polygon) => Editor.convertRegion(polygon));
        this.state = {regions: polygons, items: window.__REGIONS__, fields: window.__FIELDS__,
            checked: new Set(polygons.reduce(
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
                    regions.push(Editor.convertRegion(obj));
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
                region.items = Editor.attachItems(region.items, id, items);
            }
            return region;
        });
        return regions;
    }

    loadItems = (id) => {
        fetch(`/regions/${id}/items/`).then(response => {
            response.json().then(items => {
                let regions = Editor.attachItems(this.state.items, id, items);
                this.setState({...this.state, items: regions});
            });
        });
    };

    handleSubmit = (event) => {
        event.preventDefault();
        let center = this.map.getCenter();
        let data = new FormData(event.target);
        data.set('center', `SRID=4326;POINT(${center.lng()} ${center.lat()})`);
        data.set('zoom', this.map.getZoom());
        html2canvas(document.querySelector("#map > div > div > div"), {logging: false, useCORS: true})
            .then(canvas => {data.set('image', canvas.toDataURL())})
            .then(() => {CSRFfetch(window.location.href, {method: 'POST', body: data})});
    };

    saveMapRef = (map) => {
        this.map = map;
    };

    render() {
        return <form method="post" onSubmit={this.handleSubmit}>
            <div className="flex-container">
                <Tree {...this.state} onChange={this.onChange} loadItems={this.loadItems}
                      className="tree-visualization" checkboxName="regions"/>
                <div className="map-visualization">
                    <div className="form-group">
                        <label htmlFor="id_publish">Publish:</label>
                        <input type="checkbox" name="is_published" className="form-control" id="id_publish"
                               defaultChecked={this.state.fields.is_published} />
                    </div>
                    <Map regions={this.state.regions} mapTypeId="terrain" initCallback={this.saveMapRef} />
                    <p>Position and zoom will be saved as default for that game.</p>
                    {this.state.fields.translations.map((item) =>
                        <div className="form-group" key={item.code}>
                            <label htmlFor={`id_${item.code}_name`}>{item.language} Name:</label>
                            <input type="text" name={`${item.code}_name`} className="form-control" maxLength="15"
                                   id={`id_${item.code}_name`} defaultValue={item.title}/>
                        </div>)}
                    <button className="btn btn-primary" type="submit">Save</button>
                </div>
            </div>
        </form>;
    }
}


render(<Editor />, document.getElementById('editor'));
