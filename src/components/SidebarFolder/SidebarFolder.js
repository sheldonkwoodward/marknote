import React, { Component } from 'react';
import './SidebarFolder.css';


class SidebarFolder extends Component {
  render() {    
    return (      
      <button onClick={() => this.props.onChooseFolder(this.props.folder.id)}
              className="list-group-item list-group-item-action
                         flex-column align-items-start"
      >
        <div className="d-flex w-100 justify-content-between">
          <h5 className="mb-1">{this.props.folder.title}</h5>
        </div>
        <small>{this.props.folder.id}</small>
      </button>
    );
  }
}

export default SidebarFolder;
