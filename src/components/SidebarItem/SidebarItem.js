import React, { Component } from 'react';
import './SidebarItem.css';


class SidebarItem extends Component {
  render() {
    let buttonClass = "list-group-item list-group-item-action flex-column align-items-start"
    if (this.props.note.id === this.props.current) {
      buttonClass += " active"
    }
    return (      
      <button onClick={() => this.props.onChooseNote(this.props.note.id)} className={buttonClass}>
        <div className="d-flex w-100 justify-content-between">
          <h5 className="mb-1">{this.props.note.title}</h5>
          <small>{this.props.note.timestamp}</small>
        </div>
        <p className="mb-1">{this.props.note.content}</p>
        <small>{this.props.note.id}</small>
      </button>
    );
  }
}

export default SidebarItem;
