import React, { Component } from 'react';
import './App.css';

import Editor from '../Editor/Editor';
import Navbar from '../Navbar/Navbar';
import Sidebar from '../Sidebar/Sidebar';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: null,
      currentType: null,
      draft: {},
      notes: [],
      folders: [],
    }
  }
  
  // indexing
  getIndexById(id) {
    // find note
    for (let i in this.state.notes) {
      if (this.state.notes[i].id === id) {
        return i;
      }
    }
    // find folder
    for (let i in this.state.folders) {
      if (this.state.folders[i].id === id) {
        return i;
      }
    }
    // not found
    return null;
  }
  getIndexCurrent() {
    return this.getIndexById(this.state.current);
  }
  generateId() {
    const uuidv1 = require('uuid/v1');
    let uuid = uuidv1();
    return uuid;
  }
  
  // updates
  updateTitle(title) {
    let draft = this.state.draft;
    draft.title = title;
    this.setState({draft: draft});
  }
  updateContent(content) {
    if (this.state.currentType === "folder") {
      return;
    }
    let draft = this.state.draft;
    draft.content = content;
    this.setState({draft: draft});
  }
  
  // manage notes
  chooseNote(id) {
    let draft = this.state.notes[this.getIndexById(id)];
    this.setState({draft: Object.assign({}, draft)});
    this.setState({current: id});
    this.setState({currentType: "note"});
  }
  addNote() {
    let id = this.generateId();
    let draft = {
      id: id,
      title: "",
      content: "",
      timestamp: Date.now(),
    };
    this.setState({draft: Object.assign({}, draft)});
    this.setState({current: id});
    this.setState({currentType: "note"});
  }
  saveNote() {
    if (this.state.draft.title === "") {
      alert("Title is required");
      return;
    }
    let draft = this.state.draft;
    let notes = this.state.notes;
    draft.timestamp = Date.now();
    if (this.getIndexCurrent() === null) {
      notes.unshift(Object.assign({}, draft));
    } else {
      notes[this.getIndexCurrent()] = draft;
    }
    this.setState({notes: notes});
  }
  copyCurrentNote() {
    this.copyNote(this.state.current);
  }
  copyNote(id) {
    let notes = this.state.notes;
    let note = Object.assign({},notes[this.getIndexById(id)]);
    note.id = this.generateId();
    note.title += " copy";
    note.timestamp = Date.now();
    notes.unshift(note);
    this.setState({notes: notes});
  }
  deleteCurrentNote() {
    this.deleteNote(this.state.current);
  }
  deleteNote(id) {
    let notes = this.state.notes;
    this.setState({current: null});
    notes.splice(this.getIndexById(id), 1);
    this.setState({notes: notes});
  }
  
  // manage folders
  chooseFolder(id) {
    let draft = this.state.folders[this.getIndexById(id)];
    this.setState({draft: Object.assign({}, draft)});
    this.setState({current: id});
    this.setState({currentType: "folder"});
  }
  addFolder() {
    let id = this.generateId();
    let draft = {
      id: id,
      title: "",
    };
    this.setState({draft: Object.assign({}, draft)});
    this.setState({current: id});
    this.setState({currentType: "folder"});
  }
  saveFolder() {
    if (this.state.draft.title === "") {
      alert("Title is required");
      return;
    }
    let draft = this.state.draft;
    let folders = this.state.folders;
    if (this.getIndexCurrent() === null) {
      folders.unshift(Object.assign({}, draft));
    } else {
      folders[this.getIndexCurrent()] = draft;
    }
    this.setState({folders: folders});
  }
  deleteCurrentFolder() {
    this.deleteFolder(this.state.current);
  }
  deleteFolder(id) {
    let folders = this.state.folders;
    this.setState({current: null});
    folders.splice(this.getIndexById(id), 1);
    this.setState({folders: folders});
  }
  
  // render
  render() {
    // conditional editor
    let editor = <div className="col"></div>
    if (this.state.current != null) {
      editor = <div className="col">
                  <Editor
                    draft={this.state.draft}
                    draftType={this.state.currentType}
                    onSaveNote={() => this.saveNote()}
                    onSaveFolder={() => this.saveFolder()}
                    onCopyNote={() => this.copyCurrentNote()}
                    onDeleteNote={() => this.deleteCurrentNote()}
                    onDeleteFolder={() => this.deleteFolder()}
                    onUpdateTitle={t => this.updateTitle(t)}
                    onUpdateContent={c => this.updateContent(c)}
                  />
                </div>
    }
    
    return (
      <div>
        <Navbar />
        <div className="container">
          <div className="row mt-4">
            <div className="col-4">
              <Sidebar
                current={this.state.current}
                notes={this.state.notes}
                folders={this.state.folders}
                onChooseNote={id => this.chooseNote(id)}
                onChooseFolder={id => this.chooseFolder(id)}
                onAddNote={() => this.addNote()}
                onAddFolder={() => this.addFolder()}
                onDeleteFolder={id => this.deleteFolder(id)}
              />                      
            </div>
            {editor}
          </div>
        </div>
      </div>
    );
  }
}

export default App;
