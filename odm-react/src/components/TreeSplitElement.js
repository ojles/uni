import React from 'react'
import DefaultApi from '../api/index'
import {Api} from '../api/index'
import ObjectForm from './form/ObjectForm'
import Button from './form/Button'
import {connect} from 'react-redux'
import ObjectClassSelect from './ObjectClassSelect'
import Popup from "reactjs-popup";

import './TreeSplitElement.css'

class TreeSplitElement extends React.Component {
    inputChangeCallback = (id, value) => {
        this.props.updateObjectProperty(id, value);
    }

    newObjectInputChangeCallback = (id, value) => {
        this.props.updateNewObjectProperty(id, value);
    }

    handleUpdateObject = () => {
        // Move this logic to some service.
        // Someone may forget to set sourceUrl here
        const sourceUrl = this.props.object.sourceUrl;
        DefaultApi.updateObject(this.props.object)
            .then(updatedObject => {
                updatedObject.sourceUrl = sourceUrl;
                this.props.updateObject(updatedObject);
            });
    }

    handleRemoveObject = () => {
        // TODO: test if this is working correctly
        const object = this.props.object;
        const api = new Api(object.sourceUrl);
        api.removeObjectById(object.id)
            .then(() => {
                return api.getObjectById(object.majorId);
            })
            .then((majorObject) => {
                majorObject.sourceUrl = api.apiUrl;
                this.props.removeObject(object, majorObject);
            });

        // TODO: don't forget to set other current object
    }

    handleAddObject = (closeModal) => {
        if (!this.props.newObject.clazz) {
            // TODO: replace with notification
            console.log('Please select class!');
            return;
        }

        const {object, newObject} = this.props;
        const api = new Api(object.sourceUrl);
        newObject.majorId = object.id;
        api.addObject(newObject)
            .then(addedObject => {
                addedObject.sourceUrl = object.sourceUrl;
                this.props.addNewObject(addedObject);
                closeModal();
            });
    }

    handleNewObjectClassChange = (event) => {
        this.props.updateNewObjectProperty('clazz', event.target.value);
    }

    render() {
        const {object, newObject} = this.props;
        const PopupButton = React.forwardRef(
            ({open, ...props}, ref) => (<Button {...props}/>)
        );
        return (
            <div id="object-form-wrapper">
                <ObjectForm object={object} inputChangeCallback={this.inputChangeCallback}/>
                <Button content="Update" onClick={this.handleUpdateObject}/>
                <Button content="Remove" onClick={this.handleRemoveObject}/>
                <Popup trigger={<PopupButton content="Add new"/>} position="center center" arrow={false} modal={true}>
                    {closeModal => (
                        <div>
                            <ObjectClassSelect value={newObject.clazz} optionChangeCallback={this.handleNewObjectClassChange}/>
                            <ObjectForm object={newObject} inputChangeCallback={this.newObjectInputChangeCallback}/>
                            <Button content="Submit" onClick={() => this.handleAddObject(closeModal)}/>
                        </div>
                    )}
                </Popup>
            </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        object: state.object,
        newObject: state.newObject
    };
};

const mapDispatchToProps = (dispatch) => {
    return {
        updateObject: (newObject) => {
            dispatch({
                type: 'UPDATE_OBJECT_DATA',
                payload: newObject
            })
        },
        updateObjectProperty: (id, newValue) => {
            dispatch({
                type: 'UPDATE_OBJECT_PROPERTY',
                payload: {
                    id,
                    newValue
                }
            })
        },
        updateNewObjectProperty: (id, newValue) => {
            dispatch({
                type: 'UPDATE_NEW_OBJECT_PROPERTY',
                payload: {
                    id,
                    newValue
                }
            })
        },
        addNewObject: (newObject) => {
            dispatch({
                type: 'ADD_NEW_OBJECT',
                payload: {
                    newObject
                }
            })
        },
        removeObject: (object, majorObject) => {
            dispatch({
                type: 'REMOVE_OBJECT',
                payload: {
                    object,
                    majorObject
                }
            });
        }
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(TreeSplitElement);
