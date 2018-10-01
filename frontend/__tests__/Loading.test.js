import React from 'react';
import {shallow} from 'enzyme';
import Loading from '../components/Loading';


it('shallow <Loading /> components', () => {
    const wrapper = shallow(<Loading text='test'/>);
    expect(wrapper).toMatchSnapshot();
});
