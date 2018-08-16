import React, { Component } from 'react';
import './SidebarFolder.css';


class SidebarFolder extends Component {
  render() {
    let buttonClass = "list-group-item list-group-item-action flex-column align-items-start"
    let navigateClass = "btn btn-primary"
    if (this.props.folder.id === this.props.current) {
      buttonClass += " active text-white"
      navigateClass = "btn btn-light"
    }
    
    return (      
      <a onClick={() => this.props.onChooseFolder(this.props.folder.id)}
              className={buttonClass}
      >
        <div className="d-flex w-100 justify-content-between">
          <div>
            <h5 className="mb-1">{this.props.folder.title}</h5>
            <small>/path/to/folder/</small>
          </div>
          <button 
            className={navigateClass}
            onClick={() => this.props.onNavigateForward(this.props.folder.id)}
          >
            <i className="fas fa-chevron-right"></i>
          </button>
        </div>
      </a>
    );
  }
}

export default SidebarFolder;
