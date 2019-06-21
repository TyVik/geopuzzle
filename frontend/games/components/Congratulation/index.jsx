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

  share_fb = () => {
    FB.ui({
      app_id: 1273749826026102,
      method: 'feed',
      display: 'popup',
      link: this.props.url,
      caption: this.props.share
    }, function(response){});
  };

  share_google = () => {
    window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600');
  };

  onClose = () => {
    this.setState({...this.state, show: false});
  };

  render() {
    let text = decode(this.state.text) + this.props.result + '.';
    return <Modal show={this.state.show} onHide={this.onClose} aria-labelledby="contained-modal-title-lg">
      <Modal.Header closeButton>
        <Modal.Title id="contained-modal-title-lg"><Msg id="congratulations"/></Modal.Title>
      </Modal.Header>
      <Modal.Body>{text}</Modal.Body>
      <Modal.Footer>
        <div className="pull-right">
          <a className="btn btn-social-icon btn-vk" target="_blank"
             href={"https://vk.com/share.php?url=" + this.props.url + "&title=" + text}>
            <i className="fab fa-vk" />
          </a>
          <a className="btn btn-social-icon btn-facebook"
             href="#" onClick={this.share_fb}
             target="_blank">
            <i className="fab fa-facebook" />
          </a>
          <a className="btn btn-social-icon btn-twitter"
             href={"https://twitter.com/intent/tweet?text=" + text + "&url=" + this.props.url + "&hashtags=geopuzzle"}
             target="_blank">
            <i className="fab fa-twitter" />
          </a>
        </div>
      </Modal.Footer>
    </Modal>;
  }
}


export default Congratulation;
