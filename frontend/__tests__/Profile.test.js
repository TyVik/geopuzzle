'use strict';
import React from "react";
import Profile from "../profile/index";
import {createComponentWithIntl, mountComponentWithIntl} from "./utils";
import ProfileForm from "../profile/ProfileForm";


describe('shallow <Profile /> components', () => {
    let user = {"username": "admin", "email": "admin@admin.com",
      "image": "https://d2nepmml5nn7q0.cloudfront.net/avatars/e_28d3ad97.jpg",
      "language": "en", "is_subscribed": true
    };
    let providers = [
      {"slug": "facebook", "connected": true, "label": "FB", "class": "facebook"},
      {"slug": "vk-oauth2", "connected": true, "label": "VK", "class": "vk"},
      {"slug": "google-oauth2", "connected": false, "label": "Google", "class": "google"}
    ];

  it('render', () => {
    expect(createComponentWithIntl(<Profile user={user} providers={providers}/>)).toMatchSnapshot('Profile');
  });

  it('profileFormUpdate', () => {
    global.fetch.mockResponse("{}");
    let wrapper = mountComponentWithIntl(<ProfileForm user={user}/>);
    wrapper.find('form').simulate('submit');
    expect(global.fetch).toHaveBeenCalledWith(
      'blank?section=main',
      expect.objectContaining({ method: 'POST', body: expect.any(FormData) }));
  });
});
