import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from './Navbar'

export default class AppWrapper extends React.Component {
  render() {
    // for navigation bar logic
    return (
      <div className='app-container'>
        <Navbar />
        {this.props.children}
      </div>
    )
  }
}