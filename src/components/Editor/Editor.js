import React, { Component } from 'react';
import './Editor.css';

import SimpleMDE from 'react-simplemde-editor';
import "simplemde/dist/simplemde.min.css";


class Editor extends Component {
  render() {
    return (
      <div>
        <form>
          <div className="form-group">
            <input
              onChange={t => this.props.onUpdateCurrentTitle(t.target.value)}
              value={this.props.note.title}
              type="text"
              className="form-control form-control-lg"
              placeholder="Title"
              maxLength="20"
            />
          </div>
        </form>
        <SimpleMDE
          onChange={c => this.props.onUpdateCurrentContent(c)}
          value={this.props.note.content}
          options={{
            autofocus: true,
            spellChecker: true,
          }}
        />
      </div>
    );
  }
}

export default Editor;
