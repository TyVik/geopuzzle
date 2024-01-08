'use strict';
import React from "react";
import { render } from "./utils";
import Index from "../index/index";


describe('<Index />', () => {
  let id = 0;
  let game = name => {
    id += 1;
    return {id: id, image: `${name}.jpg`, name: name, url: `/puzzle/${name}/`};
  };

  let generateGames = () => {
    let world = ["hard", "easy"].map(item => game(item));
    let parts = ["europe", "america", "asia", "africa"].map(item => game(item));
    return [
      {items: {world: world, parts: parts}, name: "puzzle", link: "puzzle_map", caption: "Puzzle"},
      {items: {world: world, parts: parts}, name: "quiz", link: "quiz_map", caption: "Quiz"}
    ];
  };

  beforeEach(() => {
      global.fetch.resetMocks();
  });

  test('render', async () => {
    global.fetch.mockResponse(JSON.stringify(["belarus", "russia", "us", "uk"].map(item => game(item))));

    const wrapper = render(<Index games={generateGames()}/>);
    expect(wrapper.getAllByRole('tab').length).toBe(2);
    expect(wrapper.getAllByRole('img').length).toBe(6);

    // act(() => {
    //   const loadMore = wrapper.getByText('index.loadMore');
    //   fireEvent.click(loadMore);
    //   screen.debug();
    //   let headers = new Headers();
    //   headers.append("X-CSRFTOKEN", "csrf");
    //   expect(global.fetch).toHaveBeenCalledWith('/index/scroll/puzzle/?limit=24&ids=', {"credentials": "same-origin", "headers": headers});
    //   expect(wrapper.getAllByRole('img').length).toBe(10);
    // });
  });
});
