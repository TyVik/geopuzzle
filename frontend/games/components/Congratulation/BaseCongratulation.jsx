'use strict';
import React from "react";
import {Button, Modal} from 'react-bootstrap';
import {FormattedMessage as Msg} from "react-intl";

import "./index.css";


class BaseCongratulation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {show: true, url: location.href};
  }

  shareFb = () => {
    FB.ui({
      app_id: 1273749826026102,
      method: 'feed',
      display: 'popup',
      link: this.state.url,
      caption: this.props.share
    }, function(response){});
  };

  onClose = () => {
    this.setState(state => ({...state, show: false}));
  };

  getText() {
    let time = new Date(this.props.options.score * 1000);
    let params = {'name': window.__GAME__.name, 'subjects': window.__GAME__.parts, 'time': time.toLocaleTimeString('ru-RU', {timeZone: 'UTC'})};
    return this.props.intl.formatMessage({id: this.props.text}, params);
  }

  header() {
    return <Msg id="congratulations"/>;
  }

  render() {
    let text = this.getText();
    return <Modal show={this.state.show} onHide={this.onClose} aria-labelledby="contained-modal-title-lg">
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-lg">{this.header()}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div>{text}</div>
      </Modal.Body>
      <Modal.Footer>
        <iframe src="https://www.patreon.com/platform/iframe?widget=become-patron-button&amp;redirectURI=https%3A%2F%2Fgeopuzzle.org%2Fpuzzle%2Fworkshop%2F&amp;creatorID=11576139"
                className="patreon-widget"></iframe>
        <div className="pull-right">
          <a className="btn btn-social-icon btn-vk" target="_blank" rel="noopener noreferrer"
             href={"https://vk.com/share.php?url=" + this.state.url + "&title=" + text}>
            <i className="fab fa-vk" />
          </a>
          <a className="btn btn-social-icon btn-facebook"
             href="#" onClick={this.shareFb}
             target="_blank" rel="noopener noreferrer">
            <i className="fab fa-facebook" />
          </a>
          <a className="btn btn-social-icon btn-twitter"
             href={"https://twitter.com/intent/tweet?text=" + text + "&url=" + this.state.url + "&hashtags=geopuzzle"}
             target="_blank" rel="noopener noreferrer">
            <i className="fab fa-twitter" />
          </a>
        </div>
      </Modal.Footer>
    </Modal>;
  }
}


export default BaseCongratulation;
