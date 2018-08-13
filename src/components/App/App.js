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
  
  // update notes
  updateCurrentTitle(title) {
    let notes = this.state.notes;
    notes[this.getIndexCurrent()].title = title;
    this.setState({notes: notes});
  }
  updateCurrentContent(content) {
    let notes = this.state.notes;
    notes[this.getIndexCurrent()].content = content;
    this.setState({notes: notes});
  }
  updateCurrentTimestamp() {
    let notes = this.notes;
    notes[this.getIndexCurrent()].timestamp = Date.now();
  }
  
  // manage notes
  chooseNote(id) {
    this.setState({current: id});
  }
  addNote() {
    let notes = this.state.notes;
    let note = {
      id: this.generateId(),
      title: "",
      content: "",
      timestamp: Date.now(),
    };
    notes.push(note);
    this.setState({notes: notes});
    this.setState({current: note.id})
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
    folders.push(folder);
    this.setState({folders: folders});
  }
  deleteFolder(id) {
    
  }
  
  // render
  render() {
    let editor = <div className="col"></div>
    if (this.getIndexCurrent() != null) {
      editor = <div className="col">
                  <Editor
                    note={this.state.notes[this.getIndexCurrent()]}
                    onUpdateCurrentTitle={t => this.updateCurrentTitle(t)}
                    onUpdateCurrentContent={c => this.updateCurrentContent(c)}
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
              onAddNote={() => this.addNote()}
              onDeleteNote={id => this.deleteNote(id)}
              onChooseFolder={id => this.chooseFolder(id)}
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
