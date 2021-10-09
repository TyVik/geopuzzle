'use strict';
import React from "react";
import {Nav, Tab} from "react-bootstrap";


export default class GameTabs extends React.Component {
  renderTab = (game) => {
    let className = `${game.name}-tab`;
    return <Nav.Item key={game.name}>
      <Nav.Link eventKey={game.name} className={className}>{game.caption}</Nav.Link>
    </Nav.Item>;
  }

  render() {
    return <Tab.Container defaultActiveKey="puzzle" id="indexTab" mountOnEnter onSelect={this.props.tabChanged}>
      <Nav fill variant="tabs">
        {this.props.games.map(item => this.renderTab(item))}
      </Nav>
      <Tab.Content>
        {this.props.games.map(item => this.props.tabContent(item))}
      </Tab.Content>
    </Tab.Container>;
  }
}
