import React, { Component } from 'react';
import './Sidebar.css';

import SidebarItem from '../SidebarItem/SidebarItem';


class Sidebar extends Component {
  render() {
    return (
      <div className="Sidebar">
        <h1>Sidebar</h1>
        <ol>
          <li>
            <SidebarItem />
          </li>
          <li>
            <SidebarItem />
          </li>
          <li>
            <SidebarItem />
          </li>
        </ol>
      </div>
    );
  }
}

export default Sidebar;
