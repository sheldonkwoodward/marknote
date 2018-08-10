import React, { Component } from 'react';
import './Sidebar.css';

import SidebarItem from '../SidebarItem/SidebarItem';


class Sidebar extends Component {
  render() {
    const notes = this.props.notes.map((n) => 
                  <SidebarItem
                    key={n.id}
                    note={n}
                    onChooseNote={n => this.props.onChooseNote(n)}
                    current={this.props.current}
                  />);
    return (
      <div className="list-group">
        {notes}
      </div>
    );
  }
}

export default Sidebar;
