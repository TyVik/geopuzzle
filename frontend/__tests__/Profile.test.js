'use strict';
import React from "react";
import Profile from "../profile/index";
import {createComponentWithIntl} from "./utils";


describe('shallow <Profile /> components', () => {
  it('render', () => {
    let user = {"username": "admin", "email": "admin@admin.com",
      "image": "https://d2nepmml5nn7q0.cloudfront.net/avatars/e_28d3ad97.jpg",
      "language": "en", "is_subscribed": true
    };
    let providers = [
      {"slug": "facebook", "connected": true, "label": "FB", "class": "facebook"},
      {"slug": "vk-oauth2", "connected": true, "label": "VK", "class": "vk"},
      {"slug": "google-oauth2", "connected": false, "label": "Google", "class": "google"}
    ];
    expect(createComponentWithIntl(<Profile user={user} providers={providers}/>)).toMatchSnapshot('Profile');
  });
});
