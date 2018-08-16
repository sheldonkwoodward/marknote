import React, { Component } from 'react';
import './Sidebar.css';

import SidebarItem from '../SidebarItem/SidebarItem';
import SidebarFolder from '../SidebarFolder/SidebarFolder';


class Sidebar extends Component {
  sortNotes(a, b) {
    if (a.timestamp < b.timestamp)
      return -1;
    if (a.timestamp > b.timestamp)
      return 1;
    return 0;
  }
  sortFolders(a, b) {
    if (a.title < b.title)
      return -1;
    if (a.title > b.title)
      return 1;
    return 0;
  }
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
                    onChooseFolder={id => this.props.onChooseFolder(id)}
                    onNavigateForward={id => this.props.onNavigateForward(id)}
                    current={this.props.current}
                  />);

    // sidebar options
    let folderOptions = <div></div>
    let noteOptions = <div></div> 
       
    // hiding
    if (folders.length > 0) {
      folderOptions = <div>
                        <small><strong>folders</strong></small>
                        <div className="list-group mb-3">
                          {folders}
                        </div>
                      </div>
    }
    if (notes.length > 0) {
      noteOptions = <div>
                      <small><strong>notes</strong></small>
                      <div className="list-group">
                        {notes}
                      </div>
                    </div>
    }
    
    // sorting
    notes.sort(this.sortNodes);
    folders.sort(this.sortFolders);
    
    return (
      <div>
        <div className="btn-group mb-3" role="group">
          <button className="btn btn-primary"
                  onClick={() => this.props.onNavigateBack()}
          >
            <i className="fas fa-chevron-left"></i>
          </button>          
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
          <button className="btn btn-primary">
            <i className="fas fa-sync-alt"></i>
          </button>
          <button className="btn btn-primary">
            <i className="fas fa-moon"></i>
          </button>
          <button className="btn btn-primary">
            <i className="fas fa-book-open"></i>
          </button>
        </div>
        {folderOptions}
        {noteOptions}
      </div>
    );
  }
}

export default Sidebar;
