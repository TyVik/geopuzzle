'use strict';
import React from "react";
import {Row, Col} from "react-bootstrap";
import {FormattedMessage as Msg} from "react-intl";


export default class SocialLinksForm extends React.Component {
  LINK_URL = '/accounts/social/login/';
  UNLINK_URL = '/accounts/social/disconnect/';

  constructor(props) {
    super(props);
    this.links = window.__PROVIDERS__;
  }

  render_link = (item) => {
    return <a href={`${this.LINK_URL}${item.slug}/`} className={`btn btn-lg btn-${item.class} btn-block`}>{item.label}</a>;
  };

  render_unlink = (item) => {
    return <React.Fragment>
      <div className={`btn btn-lg btn-${item.class} btn-block`}>{item.label}</div>
      <a href={`${this.UNLINK_URL}${item.slug}/`} className="text-center d-block"><Msg id="unlink"/></a>
    </React.Fragment>;
  };

  render() {
    return <Row>
      {this.links.map(item => {
        return <Col key={item.slug} sm={4} className="p-2">
          {item.connected ? this.render_unlink(item) : this.render_link(item)}
        </Col>;
      })}
    </Row>;
  }
}
