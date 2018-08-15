import React, { Component } from 'react';
import './SidebarFolder.css';


class SidebarFolder extends Component {
  render() {
    let buttonClass = "list-group-item list-group-item-action flex-column align-items-start"
    if (this.props.folder.id === this.props.current) {
      buttonClass += " active text-white"
    }
    
    return (      
      <a onClick={() => this.props.onChooseFolder(this.props.folder.id)}
              className={buttonClass}
      >
        <div className="d-flex w-100 justify-content-between">
          <h5 className="mb-1">{this.props.folder.title}</h5>
        </div>
        <small>/path/to/folder/</small>
      </a>
    );
  }
}

export default SidebarFolder;
