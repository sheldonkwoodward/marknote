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
  render() {    
    return (
      <div className="container">
        <div className="row">
          <Header />
        </div>
        <br />
        <div className="row">
          <div className="col-4">
            <Sidebar current={this.state.current} notes={this.state.notes} onChooseNote={n => this.chooseNote(n)} />                      
          </div>
          <div className="col">
            <Editor />
          </div>
        </div>

      </div>
    );
  }
}

export default App;
