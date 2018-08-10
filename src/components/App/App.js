import React, { Component } from 'react';
import './App.css';

import Editor from '../Editor/Editor';
import Header from '../Header/Header';
import Sidebar from '../Sidebar/Sidebar';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      current: 0,
      notes: [
        {
          id: 0,
          title: "My note 0",
          content: "The notes content goes here.",
          timestamp: "timestamp",
          status: "most recent",
        },
        {
          id: 1,
          title: "My note 1",
          content: "The notes content goes here.",
          timestamp: "timestamp",
          status: "most recent",
        },
        {
          id: 2,
          title: "My note 2",
          content: "The notes content goes here.",
          timestamp: "timestamp",
          status: "most recent",
        },
      ],
    }
  }
  chooseNote(id) {
    this.setState({current: id});
  }
  updateTitle(title) {    
    let state = this.state;
    state.notes[state.current].title = title;
    this.setState(state);
  }
  updateContent(content) {
    let state = this.state;
    state.notes[state.current].content = content;
    this.setState(state);
  }
  render() {    
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
              onChooseNote={n => this.chooseNote(n)}
            />                      
          </div>
          <div className="col">
            <Editor
              note={this.state.notes[this.state.current]}
              onUpdateTitle={t => this.updateTitle(t)}
              onUpdateContent={c => this.updateContent(c)}
            />
          </div>
        </div>

      </div>
    );
  }
}

export default App;
