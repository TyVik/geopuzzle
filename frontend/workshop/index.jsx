'use strict';
import 'url-search-params-polyfill';
import React from "react";
import AsyncSelect from 'react-select/async';
import Select from 'react-select';
import {FormattedMessage as Msg} from 'react-intl';
import GameScrollList from "../components/GamesScrollList/GameScrollList";
import {CSRFfetch} from "../utils";
import {debounce, defer} from "lodash";


class Workshop extends React.Component {
  constructor(props) {
    super(props);
    this.orderOptions = props.orderOptions;
    this.state = props.state;
  }

  onChangeSearch = debounce((value) => {
    this.setState(state => ({...state, search: value || ''}));
  }, 300);

  loadOptions = (field, inputValue, callback) => {
    if ((inputValue === '') && (field !== 'tag')) {
      return callback([]);
    }
    defer(async () => {
      let baseUrl = null;
      switch (field) {
        case 'tag':
          baseUrl = '/workshop/tags/';
          break;
        case 'user':
          baseUrl = '/accounts/users/';
          break;
      }
      let response = await CSRFfetch(`${baseUrl}?name=${inputValue}`, {});
      callback(await response.json());
    });
  };

  onChange = (field, event) => {
    let state = {...this.state};
    state[field] = (event === null) ? null : event.value;
    this.setState(state);
  };

  render_controls() {
    return <form className="row justify-content-between">
      <div className="form-group col-md-7 col-sm-12">
        <label htmlFor="search-label"><Msg id="search"/>:</label>
          <input type="text" className="form-control" maxLength="50" id="search-input"
                 onChange={(event) => this.onChangeSearch(event.target.value)} />
      </div>
      <div className="form-group col-md-5 col-sm-12">
        <label htmlFor="order-label"><Msg id="orderBy"/>:</label>
        <Select isClearable options={this.orderOptions} onChange={(event) => this.onChange('order', event)} />
      </div>
      <div className="form-group col-md-6 col-sm-12">
        <label htmlFor="search-label"><Msg id="tag"/>:</label>
          <AsyncSelect cacheOptions defaultOptions isClearable
                       loadOptions={(inputValue, callback) => this.loadOptions('tag', inputValue, callback)}
                       onChange={(event) => this.onChange('tag', event)} />
      </div>
      <div className="form-group col-md-6 col-sm-12">
        <label htmlFor="search-label"><Msg id="user"/>:</label>
          <AsyncSelect cacheOptions defaultOptions isClearable
                       loadOptions={(inputValue, callback) => this.loadOptions('user', inputValue, callback)}
                       onChange={(event) => this.onChange('user', event)} />
      </div>
    </form>;
  }

  currentUrl() {
    let params = new URLSearchParams();
    ['search', 'tag', 'user', 'order'].forEach(item => {
      if ((this.state[item] !== null) && (this.state[item].length > 0)) {
        params.set(`${item}`, this.state[item]);
      }
    });
    let result = params.toString();
    return `${location.href}items/?${result}`;
  }

  render() {
    return <React.Fragment>
      {this.render_controls()}
      <GameScrollList url={this.currentUrl()}/>
    </React.Fragment>;
  }
}

export default Workshop;
