import React from 'react';
import Navbar from './Navbar'

export default class AppWrapper extends React.Component {
  render() {
    // for navigation bar logic
    return (
      <div>
        <Navbar />
        {this.props.children}
      </div>
    )
  }
}