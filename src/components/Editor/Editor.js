import React, { Component } from 'react';
import './Editor.css';

import SimpleMDE from 'react-simplemde-editor';
import "simplemde/dist/simplemde.min.css";


class Editor extends Component {
  render() {
    // save folder button
    let saveButton = <button className="btn btn-lg btn-primary"
                              onClick={() => this.props.onSaveFolder()}
                              type="button"
                      >
                        <i className="fas fa-save"></i>
                      </button>
    // disabled copy folder button
    let copyButton = <button className="btn btn-lg btn-primary"
                             type="button"
                             disabled
                     >
                       <i className="fas fa-copy"></i>
                     </button>
    // delete folder button
    let deleteButton = <button className="btn btn-lg btn-danger"
                               onClick={() => this.props.onDeleteFolder()}
                               type="button"
                       >
                         <i className="fas fa-trash"></i>
                       </button>
    // disabled editor
    let simpleMDE = <div></div>
    
    // check if note is being edited
    if (this.props.draftType === "note") {
      // save note button
      saveButton = <button className="btn btn-lg btn-primary"
                            onClick={() => this.props.onSaveNote()}
                            type="button"
                    >
                      <i className="fas fa-save"></i>
                    </button>
      // copy note button
      copyButton = <button className="btn btn-lg btn-primary"
                           onClick={() => this.props.onCopyNote()}
                           type="button"
                   >
                     <i className="fas fa-copy"></i>
                   </button>
      // delete note button
      deleteButton = <button className="btn btn-lg btn-danger"
                             onClick={() => this.props.onDeleteNote()}
                             type="button"
                     >
                       <i className="fas fa-trash"></i>
                     </button>
      // editor
      simpleMDE = <SimpleMDE
                    onChange={c => this.props.onUpdateContent(c)}
                    value={this.props.draft.content}
                    options={{
                      autofocus: true,
                      spellChecker: true,
                    }}
                  />
    }
    
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
                maxLength="30"
              />
            </div>
            <div className="btn-group form-group">
              {saveButton}
              {copyButton}
              {deleteButton}
            </div>
          </div>
        </form>
        {simpleMDE}
      </div>
    );
  }
}

export default Editor;
