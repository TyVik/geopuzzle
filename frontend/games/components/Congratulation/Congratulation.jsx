'use strict';
import React from "react";
import {Modal} from 'react-bootstrap';
import {decode} from 'he';
import {FormattedMessage as Msg} from "react-intl";


class Congratulation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {...window.__CONGRATULATION__, show: true};
  }

  shareFb = () => {
    FB.ui({
      app_id: 1273749826026102,
      method: 'feed',
      display: 'popup',
      link: this.props.url,
      caption: this.props.share
    }, function(response){});
  };

  onClose = () => {
    this.setState(state => ({...state, show: false}));
  };

  getTime() {
    let time = new Date(Date.now() - this.props.startTime);
    return (time > 24 * 60 * 60 * 1000) ? <Msg id="timeOverhead"/> : time.toLocaleTimeString('ru-RU', {timeZone: 'UTC'});
  }

  getText() {
    return decode(this.state.text) + this.getTime() + '.';
  }

  render() {
    let text = this.getText();
    return <Modal show={this.state.show} onHide={this.onClose} aria-labelledby="contained-modal-title-lg">
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-lg"><Msg id="congratulations"/></Modal.Title>
      </Modal.Header>
      <Modal.Body>{text}</Modal.Body>
      <Modal.Footer>
        <div className="pull-right">
          <a className="btn btn-social-icon btn-vk" target="_blank" rel="noopener noreferrer"
             href={"https://vk.com/share.php?url=" + this.props.url + "&title=" + text}>
            <i className="fab fa-vk" />
          </a>
          <a className="btn btn-social-icon btn-facebook"
             href="#" onClick={this.shareFb}
             target="_blank" rel="noopener noreferrer">
            <i className="fab fa-facebook" />
          </a>
          <a className="btn btn-social-icon btn-twitter"
             href={"https://twitter.com/intent/tweet?text=" + text + "&url=" + this.props.url + "&hashtags=geopuzzle"}
             target="_blank" rel="noopener noreferrer">
            <i className="fab fa-twitter" />
          </a>
        </div>
      </Modal.Footer>
    </Modal>;
  }
}


export default Congratulation;
