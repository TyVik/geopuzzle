'use strict';
import 'url-search-params-polyfill';
import React from "react";
import AsyncSelect from 'react-select/async';
import Select from 'react-select';
import {FormattedMessage as Msg} from 'react-intl';
import GameScrollList from "../components/GamesScrollList";
import {CSRFfetch} from "../utils";
import {debounce} from "lodash";


class Workshop extends React.Component {
  constructor(props) {
    super(props);
    this.order_options = window.__ORDER__.map(item => {return {value: item[0], label: item[1]}});
    this.state = {search: '', _search: '', order: null, tag: null, user: null};
  }

  applySearch = debounce(() => {
    this.setState(state => ({...state, search: state['_search']}));
  }, 300);

  onChangeSearch = (event) => {
    let value = event && event.target.value || '';
    this.setState(state => ({...state, _search: value}), () => {
      this.applySearch();
    });
  };

  loadOptions = (field, inputValue, callback) => {
    if ((inputValue === '') && (field !== 'tag')) {
      return callback([]);
    }
    setImmediate(async () => {
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
                 onChange={this.onChangeSearch} value={this.state._search} />
      </div>
      <div className="form-group col-md-5 col-sm-12">
        <label htmlFor="order-label"><Msg id="orderBy"/>:</label>
        <Select isClearable options={this.order_options} onChange={(event) => this.onChange('order', event)} />
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
    ['search', 'tag', 'user', 'order'].map(item => {
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
