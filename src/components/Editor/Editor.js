import React, { Component } from 'react';
import './Editor.css';

import SimpleMDE from 'react-simplemde-editor';
import "simplemde/dist/simplemde.min.css";


class Editor extends Component {
  render() {
    return (
      <div>
        <form>
          <div className="form-row">
            <div className="form-group col mr-2">
              <input
                onChange={t => this.props.onUpdateCurrentTitle(t.target.value)}
                value={this.props.note.title}
                type="text"
                className="form-control form-control-lg"
                placeholder="Title"
                maxLength="20"
              />
            </div>
            <div className="btn-group form-group">
              <button className="btn btn-lg btn-primary"
                      onClick={() => this.props.onDeleteNote(this.props.current)}
              >
                <i className="fas fa-copy"></i>
              </button>
              <button className="btn btn-lg btn-danger"
                      onClick={() => this.props.onDeleteNote(this.props.current)}
              >
                <i className="fas fa-trash"></i>
              </button>
            </div>
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
