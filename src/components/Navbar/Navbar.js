import React, { Component } from 'react';
import './Navbar.css';


class Navbar extends Component {
  render() {
    return(
      <nav className="navbar navbar-dark bg-primary">
        <a className="navbar-brand" href="#">Marknote</a>
      </nav>
    );
  }
}

export default Navbar;
