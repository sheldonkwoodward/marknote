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
                onChange={t => this.props.onUpdateTitle(t.target.value)}
                value={this.props.draft.title}
                type="text"
                className="form-control form-control-lg"
                placeholder="Title"
                maxLength="20"
              />
            </div>
            <div className="btn-group form-group">
              <button className="btn btn-lg btn-primary"
                      onClick={() => this.props.onSaveNote(this.props.draft)}
                      type="button"
              >
                <i className="fas fa-save"></i>
              </button>
              <button className="btn btn-lg btn-primary"
                      // onClick={() => this.props.onDeleteNote(this.props.current)}
                      type="button"
              >
                <i className="fas fa-copy"></i>
              </button>
              <button className="btn btn-lg btn-danger"
                      // onClick={() => this.props.onDeleteNote(this.props.current)}
                      type="button"
              >
                <i className="fas fa-trash"></i>
              </button>
            </div>
          </div>
        </form>
        <SimpleMDE
          onChange={c => this.props.onUpdateContent(c)}
          value={this.props.draft.content}
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
