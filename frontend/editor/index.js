'use strict';
import React from "react";
import Toggle from 'react-toggle';
import Map from '../components/Map';
import Tree from "./Tree";
import {decodePolygon, CSRFfetch} from "../utils";
import localization from "../localization";
import html2canvas from 'html2canvas';
import Select from "react-select";


class Editor extends React.Component {
  MAX_REGION_COUNT = 150;

  constructor(props) {
    super(props);
    let polygons = window.__CHECKED__.map((polygon) => Editor.convertRegion(polygon));
    this.state = {
      regions: polygons,
      items: window.__REGIONS__,
      fields: window.__FIELDS__,
      checked: new Set(polygons.reduce((acc, item) => {acc.push(item.id); return acc;}, [])),
      progress: null, exception: false
    };
    this.tags = window.__TAGS__.map(x => {return {label: x[1], value: x[0]}});
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
    let bounds = this.map.getBounds();
    let data = new FormData(event.target);
    this.setState({...this.state, progress: 20});
    data.set('is_published', this.state.fields.is_published);
    data.set('center', `SRID=4326;POINT(${center.lng()} ${center.lat()})`);
    data.set('zoom', this.map.getZoom());
    data.set('bounds', [bounds.getNorthEast().lat(), bounds.getNorthEast().lng(),
                        bounds.getSouthWest().lat(), bounds.getSouthWest().lng()].join(','));
    this.setState({...this.state, progress: 30});
    html2canvas(document.querySelector("#map > div > div > div"), {logging: false, useCORS: true})
      .then(canvas => {
        this.setState({...this.state, progress: 60});
        data.set('image', canvas.toDataURL())
      })
      .then(() => {
        this.setState({...this.state, progress: 80});
        CSRFfetch(window.location.href, {method: 'POST', body: data})
          .then(response => {
            this.setState({...this.state, progress: 100});
            if (response.status === 200) {
              response.json().then(json => {
                window.location.href = json.url;
              });
            } else {
              this.setState({...this.state, progress: null, exception: true});
            }
          })
          .catch(() => {
            this.setState({...this.state, progress: null, exception: true});
          });
      });
  };

  saveMapRef = (map) => {
    this.map = map;
  };

  togglePublish = () => {
    let fields = this.state.fields;
    fields.is_published = !fields.is_published;
    this.setState({...this.state, fields: fields});
  };

  renderLocales() {
    return <div className="panel panel-default">
      <div className="panel-heading">{localization.localization}:</div>
      <div className="panel-body form-horizontal">
        {this.state.fields.translations.map((item) =>
          <div className="form-group" key={item.code}>
            <label htmlFor={`id_${item.code}_name`} className="control-label col-sm-3">{localization[`${item.code}Title`]}:</label>
            <div className="col-sm-9">
              <input type="text" name={`${item.code}_name`} className="form-control" maxLength="50"
                     id={`id_${item.code}_name`} defaultValue={item.title}/>
            </div>
          </div>)}
      </div>
    </div>;
  }

  renderPublish() {
    let title = this.state.fields.is_published ? localization.publishedToAll : localization.publishedToMe;
    return <div className="panel panel-default">
      <div className="panel-heading">{localization.publish}:</div>
      <div className="panel-body form-horizontal">
        <div className="form-group" key="is_published">
          <Toggle checked={this.state.fields.is_published} onChange={this.togglePublish} id="is_published"/>
          <label htmlFor='is_published'>{title}</label>
        </div>
        <div className="form-group" key="tags">
          <label htmlFor="id_tags" className="control-label col-sm-2">{localization['tags']}:</label>
          <div className="col-sm-10">
            <Select name="tags" options={this.tags} isMulti/>
          </div>
        </div>
      </div>
    </div>;
  }

  render() {
    return <form method="post" onSubmit={this.handleSubmit}>
      <div className="flex-container">
        <div className="panel panel-default">
          <div className="panel-heading">{localization.availableRegions}:</div>
          <div className="panel-body">
            {this.state.checked.size >= this.MAX_REGION_COUNT &&
              <div className="alert alert-danger" role="alert">{localization.tooManyRegions}</div>}
            <Tree {...this.state} onChange={this.onChange} loadItems={this.loadItems}
                  className="tree-visualization" checkboxName="regions" showCheckbox={false}/>
          </div>
        </div>
        <div className="map-visualization">
          {this.renderPublish()}
          {this.renderLocales()}
          <div className="panel panel-default">
            <div className="panel-heading">{localization.preview}:</div>
            <div className="panel-body square-container">
              <Map regions={this.state.regions} mapTypeId="terrain" initCallback={this.saveMapRef} showMap={true}/>
            </div>
            <p>{localization.previewWarning}</p>
          </div>
          {this.state.progress &&
            <div className="progress">
              <div className="progress-bar progress-bar-striped active" role="progressbar"
                   aria-valuenow={this.state.progress} aria-valuemin="0" aria-valuemax="100"
                   style={{width: this.state.progress + '%'}}>
              </div>
            </div>}
          {this.state.exception && this.state.progress === null &&
            <div className="save-exception">
              {localization.formatString(localization.bugReport, <a href="mailto:tyvik8@gmail.com?&subject=GeoPuzzle%20Exception">email me</a>)}
            </div>}
          {this.state.checked.size < this.MAX_REGION_COUNT &&
            <button className="btn btn-primary" type="submit">{localization.save}</button>}
        </div>
      </div>
    </form>;
  }
}


export default Editor;
