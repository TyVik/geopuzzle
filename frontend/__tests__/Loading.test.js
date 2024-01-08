'use strict';
import React from 'react';
import Loading from '../components/Loading';
import {render, screen} from "./utils";


test.each([
  [true, "loadingError"],
  [false, "loading"],
])("<Loading /> %p", async (hasError, str) => {
  render(<Loading hasError={hasError}/>);
  expect(screen.getByRole("heading").textContent).toBe(str);
});
