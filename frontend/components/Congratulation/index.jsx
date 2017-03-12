'use strict';
import React from "react";
import {connect} from "react-redux";
import {closeCongratulation} from "../../actions";
import {Modal, Button} from 'react-bootstrap';
import localization from '../../localization';


class Congratulation extends React.Component {
    constructor(props) {
        super(props);
        this.closeSelf = this.closeSelf.bind(this);
        this.share_fb = this.share_fb.bind(this);
        this.share_google = this.share_google.bind(this);
    }

    closeSelf() {
        this.props.dispatch(closeCongratulation());
    }

    share_fb() {
        FB.ui({
            app_id: 1273749826026102,
            method: 'feed',
            display: 'popup',
            link: this.props.url,
            caption: this.props.share
        }, function(response){});
    }

    share_google() {
        window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600');
    }

    render() {
        return (
            <Modal show={this.props.show} onHide={this.closeSelf} bsSize="large" aria-labelledby="contained-modal-title-lg">
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-lg">{localization.congratulations}</Modal.Title>
                </Modal.Header>
                <Modal.Body>{this.props.template}: {this.props.text}.</Modal.Body>
                <Modal.Footer>
                    <p className="pull-left" style={{display: "inline-block", margin: "7px 0"}}>{this.props.share}.</p>
                    <div className="pull-right">
                        <a className="btn btn-social-icon btn-vk" target="_blank"
                           href={"https://vk.com/share.php?url=" + this.props.url + "&title=" + this.props.share}><span className="fa fa-vk"></span></a>
                        <a className="btn btn-social-icon btn-facebook"
                           href="#" onClick={this.share_fb}
                           target="_blank"><span className="fa fa-facebook"></span></a>
                        <a className="btn btn-social-icon btn-twitter"
                           href={"https://twitter.com/intent/tweet?text=" + this.props.share + "&url=" + this.props.url + "&hashtags=geopuzzle"}
                           target="_blank"><span className="fa fa-twitter"></span></a>
                        <a href={"https://plus.google.com/share?url=" + this.props.url } onClick={this.share_google}><img
  src="https://www.gstatic.com/images/icons/gplus-32.png" alt="Share on Google+"/></a>
                    </div>
                </Modal.Footer>
            </Modal>
        );
    }
};


export default connect(state => (state.congratulation))(Congratulation);
