'use strict';

import {shuffle} from "../games/utils";

it('test shuffle', () => {
  let array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0];
  expect(shuffle([...array])).not.toBe(array);
});
