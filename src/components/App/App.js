import React, { Component } from 'react';
import './App.css';

import Editor from '../Editor/Editor';
import Header from '../Header/Header';
import Sidebar from '../Sidebar/Sidebar';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: null,
      draft: {},
      notes: [],
      folders: [],
    }
  }
  
  // indexing
  getIndexById(id) {
    for (let i in this.state.notes) {
      if (this.state.notes[i].id === id) {
        return i;
      }
    }
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
  
  // updating notes
  saveNote() {
    if (this.state.draft.title === "") {
      alert("Title is required");
      return;
    }
    let draft = this.state.draft;
    let notes = this.state.notes;
    let note = this.state.notes[this.getIndexCurrent()];
    draft.timestamp = Date.now();
    if (this.getIndexCurrent() === null) {
      notes.unshift(Object.assign({}, draft));
    } else {
      notes[this.getIndexCurrent()] = draft;
    }
    this.setState({notes: notes});
  }
  updateTitle(title) {
    let draft = this.state.draft;
    draft.title = title;
    this.setState({draft: draft});
  }
  updateContent(content) {
    let draft = this.state.draft;
    draft.content = content;
    this.setState({draft: draft});
  }
  
  // manage notes
  chooseNote(id) {
    let draft = this.state.notes[this.getIndexById(id)];
    this.setState({draft: Object.assign({}, draft)});
    this.setState({current: id});
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
    
  }
  addFolder() {
    let folders = this.state.folders;
    let folder = {
      id: this.generateId(),
      title: "Folder",
    };
    folders.unshift(folder);
    this.setState({folders: folders});
  }
  deleteFolder(id) {
    
  }
  
  // render
  render() {
    let editor = <div className="col"></div>
    if (this.state.current != null) {
      editor = <div className="col">
                  <Editor
                    draft={this.state.draft}
                    onSaveNote={() => this.saveNote()}
                    onCopyNote={() => this.copyCurrentNote()}
                    onDeleteNote={() => this.deleteCurrentNote()}
                    onUpdateTitle={t => this.updateTitle(t)}
                    onUpdateContent={c => this.updateContent(c)}
                  />
                </div>
    }
    
    return (
      <div className="container">
        <div className="row">
          <Header />
        </div>
        <br />
        <div className="row">
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
    );
  }
}

export default App;
