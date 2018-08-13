import React, { Component } from 'react';
import './Sidebar.css';

import SidebarItem from '../SidebarItem/SidebarItem';
import SidebarFolder from '../SidebarFolder/SidebarFolder';


class Sidebar extends Component {
  render() {
    const notes = this.props.notes.map((n) => 
                  <SidebarItem
                    key={n.id}
                    note={n}
                    onChooseNote={id => this.props.onChooseNote(id)}
                    current={this.props.current}
                  />);
    const folders = this.props.folders.map((f) => 
                  <SidebarFolder
                    key={f.id}
                    folder={f}
                    onChooseFolder={id => this.props.onChooseNote(id)}
                  />);
    return (
      <div>
        <div className="btn-group mb-3" role="group">
          <button className="btn btn-primary"
                  onClick={() => this.props.onAddNote()}
          >
            <i className="fas fa-pen"></i>
          </button>
          <button className="btn btn-primary"
                  onClick={() => this.props.onAddFolder()}
          >
            <i className="fas fa-folder"></i>
          </button>
        </div>
        <div className="list-group mb-3">
          {folders}
        </div>
        <div className="list-group">
          {notes}
        </div>
      </div>
    );
  }
}

export default Sidebar;
