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
            link: 'https://geopuzzle.org/' + this.props.slug + '/'
            // href: 'https://developers.facebook.com/docs/',
        }, function(response){});
    }

    share_google() {
        window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600');
    }

    render() {
        let time = new Date(Date.now() - this.props.time);
        let time_result = (time > 24 * 60 * 60 * 1000) ? 'more then day' : time.toLocaleTimeString([], {timeZone: 'UTC'});
        let share = this.props.share + time_result;
        let url = 'https://geopuzzle.org/maps/' + this.props.slug + '/';
        return (
            <Modal show={this.props.show} onHide={this.closeSelf} bsSize="large" aria-labelledby="contained-modal-title-lg">
                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-lg">{localization.congratulations}</Modal.Title>
                </Modal.Header>
                <Modal.Body>{this.props.template}: {this.props.text}.</Modal.Body>
                <Modal.Footer>
                    <p className="pull-left" style={{display: "inline-block", margin: "7px 0"}}>{share}.</p>
                    <div className="pull-right">
                        <a className="btn btn-social-icon btn-vk"
                           href={"https://vk.com/share.php?url=" + url + "&title=" + share}><span className="fa fa-vk"></span></a>
                        <a className="btn btn-social-icon btn-facebook"
                           href="#" onClick={this.share_fb}
                           target="_blank"><span className="fa fa-facebook"></span></a>
                        <a className="btn btn-social-icon btn-twitter"
                           href={"https://twitter.com/intent/tweet?text=" + share + "&url=" + url + "&hashtags=geopuzzle"}
                           target="_blank"><span className="fa fa-twitter"></span></a>
                        <a href={"https://plus.google.com/share?url=" + url } onClick={this.share_google}><img
  src="https://www.gstatic.com/images/icons/gplus-32.png" alt="Share on Google+"/></a>
                    </div>
                </Modal.Footer>
            </Modal>
        );
    }
};


export default connect(state => (state.congratulation))(Congratulation);
