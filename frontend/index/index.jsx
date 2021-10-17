'use strict';
import React from "react";
import {Tab} from "react-bootstrap";
import IndexPane from "./IndexPane";
import GameTabs from "../components/GameTabs";

export default class Index extends React.Component {
  tabContent = (item) => {
    return <Tab.Pane eventKey={item.name} className={`${item.name}-tab`} key={item.name}>
      <IndexPane game={item} key={item.name}/>
    </Tab.Pane>
  }

  render() {
    return <GameTabs games={this.props.games} tabContent={this.tabContent} />
  }
}

