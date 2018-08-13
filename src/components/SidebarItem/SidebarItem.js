import React, { Component } from 'react';
import './SidebarItem.css';


class SidebarItem extends Component {
  generateTimestamp() {
    let timestamp = new Date(this.props.note.timestamp);
    
    // within 24 hours
    if (Date.now() - this.props.note.timestamp < 50400) {
      return timestamp.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
      });
    }
    // within a week
    else if (Date.now() - this.props.note.timestamp < 352800) {
      return timestamp.toLocaleDateString("en-US", {
        weekday: "long",
      });
    }
    // older
    return timestamp.toLocaleDateString("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
    });
  }
  render() {
    let buttonClass = "list-group-item list-group-item-action flex-column align-items-start"
    if (this.props.note.id === this.props.current) {
      buttonClass += " active"
    }
    
    return (      
      <button onClick={() => this.props.onChooseNote(this.props.note.id)} className={buttonClass}>
        <div className="d-flex w-100 justify-content-between">
          <h5 className="mb-1">{this.props.note.title}</h5>
          <small>{this.generateTimestamp()}</small>
        </div>
        <p className="mb-1">{this.props.note.content}</p>
        <small>{this.props.note.id}</small>
      </button>
    );
  }
}

export default SidebarItem;
