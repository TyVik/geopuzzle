'use strict';
import React from "react";
import {createComponentWithIntl} from "./utils";
import Index from "../index/index";


describe('shallow <Index /> components', () => {
  let id = 0;
  let game = name => {
    id += 1;
    return {id: id, image: `${name}.jpg`, name: name, url: `/puzzle/${name}/`};
  };

  beforeAll(() => {
    let world = ["hard", "easy"].map(item => game(item));
    let parts = ["europe", "america", "asia", "africa"].map(item => game(item));
    window.__GAMES__ = [
      {items: {world: world, parts: parts}, name: "puzzle", link: "puzzle_map", caption: "Puzzle"},
      {items: {world: world, parts: parts}, name: "quiz", link: "quiz_map", caption: "Quiz"}
    ];
  });

  beforeEach(() => {
      global.fetch.resetMocks();
  });

  it('render', done => {
    global.fetch.mockResponse(JSON.stringify(["belarus", "russia", "us", "uk"].map(item => game(item))));
    let index = createComponentWithIntl(<Index/>);
    setImmediate(() => {
      expect(index).toMatchSnapshot('Index');
      let headers = new Headers();
      headers.append("X-CSRFTOKEN", "csrf");
      expect(global.fetch).toHaveBeenCalledWith('/index/scroll/puzzle/?limit=24&ids=', {"credentials": "same-origin", "headers": headers});
      done();
    });
  });
});
