'use strict';
import React from "react";
import {connect} from "react-redux";
import {Modal} from 'react-bootstrap';
import localization from '../../localization';


class Congratulation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {show: true};
    }

    closeSelf = () => {
        this.setState({show: false});
    };

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

    render() {
        let text = this.props.text + this.props.time_result + '.';
        return (
            <Modal show={this.state.show && this.props.show} onHide={this.closeSelf}
                   bsSize="large" aria-labelledby="contained-modal-title-lg">
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-lg">{localization.congratulations}</Modal.Title>
                </Modal.Header>
                <Modal.Body>{text}</Modal.Body>
                <Modal.Footer>
                    <div className="pull-right">
                        <a className="btn btn-social-icon btn-vk" target="_blank"
                           href={"https://vk.com/share.php?url=" + this.props.url + "&title=" + text}><span className="fa fa-vk" /></a>
                        <a className="btn btn-social-icon btn-facebook"
                           href="#" onClick={this.share_fb}
                           target="_blank"><span className="fa fa-facebook" /></a>
                        <a className="btn btn-social-icon btn-twitter"
                           href={"https://twitter.com/intent/tweet?text=" + text + "&url=" + this.props.url + "&hashtags=geopuzzle"}
                           target="_blank"><span className="fa fa-twitter" /></a>
                        <a href={"https://plus.google.com/share?url=" + this.props.url } onClick={this.share_google}><img
  src="https://www.gstatic.com/images/icons/gplus-32.png" alt="Share on Google+"/></a>
                    </div>
                </Modal.Footer>
            </Modal>
        );
    }
}


export default connect(state => (state.congratulation))(Congratulation);
