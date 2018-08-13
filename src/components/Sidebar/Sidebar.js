import React, { Component } from 'react';
import './Sidebar.css';

import SidebarItem from '../SidebarItem/SidebarItem';


class Sidebar extends Component {
  render() {
    const notes = this.props.notes.map((n) => 
                  <SidebarItem
                    key={n.id}
                    note={n}
                    onChooseNote={id => this.props.onChooseNote(id)}
                    current={this.props.current}
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
          <button className="btn btn-danger"
                  onClick={() => this.props.onDeleteNote(this.props.current)}
          >
            <i className="fas fa-trash"></i>
          </button>
        </div>
        <div className="list-group">
          {notes}
        </div>
      </div>
    );
  }
}

export default Sidebar;
