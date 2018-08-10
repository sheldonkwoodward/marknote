import React, { Component } from 'react';
import './App.css';

import Editor from '../Editor/Editor';
import Header from '../Header/Header';
import Sidebar from '../Sidebar/Sidebar';


class App extends Component {
  render() {
    return (
      <div className="App">
        <Header />
        <Editor />
        <Sidebar />
      </div>
    );
  }
}

export default App;
