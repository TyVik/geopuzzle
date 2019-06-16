'use strict';
import React from "react";
import {FormattedMessage as Msg} from 'react-intl';
import GameScrollList from "../components/GamesScrollList";


class Workshop extends React.Component {
  constructor(props) {
    super(props);
    this.state = {search: '', searchArg: '', tag: 0};
  }

  onChange = (event) => {
    let value = event && event.target.value || '';
    if (this.timeout !== null) {
      clearTimeout(this.timeout);
    }
    this.timeout = setTimeout(() => {this.setState({...this.state, searchArg: value})}, 300);
    this.setState({...this.state, search: value});
  };

  onChangeTag = (event) => {
    this.setState({...this.state, tag: Number(event.target.value)});
  };

  render_controls() {
    return <form className="row justify-content-between">
      <div className="form-group col-md-6 col-sm-12">
        <label htmlFor="search-label"><Msg id="search"/>:</label>
        <input type="text" className="form-control" maxLength="50" id="search-input" onChange={this.onChange} value={this.state.search} aria-describedby="basic-search-label"/>
        <small id="basic-search-label" className="form-text text-muted">Search by title, tags or author.</small>
      </div>
      <div className="form-group col-md-4 col-sm-12">
        <label htmlFor="tag-label"><Msg id="tags"/>:</label>
        <select className="form-control" id="tag-input" onChange={this.onChangeTag} value={this.state.tag} aria-describedby="tag-label">
          <option value={0}>--</option>
          {window.__TAGS__.map(tag => <option value={tag[0]} key={tag[0]}>{tag[1]}</option>)}
        </select>
      </div>
    </form>;
  }

  currentUrl() {
    let params = new URLSearchParams();
    if (this.state.searchArg) {
      params.set('search', this.state.searchArg);
    }
    if (this.state.tag > 0) {
      params.set('tag', this.state.tag);
    }
    let result = params.toString();
    result = result.length > 0 ? `${location.href}items/?${result}` : `${location.href}items/`;
    return result;
  }

  render() {
    return <React.Fragment>
      {this.render_controls()}
      <GameScrollList url={this.currentUrl()}/>
    </React.Fragment>;
  }
}

export default Workshop;
