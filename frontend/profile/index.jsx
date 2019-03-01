'use strict';
import React from "react";
import localization from "../localization";
import {Card, Col, Nav, Row, Tab} from "react-bootstrap";
import ProfileForm from "./ProfileForm";


export default class Profile extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return <Tab.Container defaultActiveKey="main">
      <Row>
        <Col md={3} sm={3} lg={2}>
          <Nav className="flex-column" variant="pills">
            <Nav.Item><Nav.Link eventKey="main">Profile</Nav.Link></Nav.Item>
          </Nav>
        </Col>
        <Col md={9} sm={9} lg={10}>
          <Tab.Content>
            <Tab.Pane eventKey="main">
              <Card>
                <Card.Header>Public profile</Card.Header>
                <Card.Body>
                  <ProfileForm fields={window.__USER__}/>
                </Card.Body>
              </Card>
            </Tab.Pane>
          </Tab.Content>
        </Col>
      </Row>
    </Tab.Container>;
  }
}
