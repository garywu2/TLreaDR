import React from 'react';
import { Redirect } from 'react-router';

const Home = (props) => (
  <div className='home'>
    <Redirect to="/category/all"></Redirect>
  </div>
)

export default Home;