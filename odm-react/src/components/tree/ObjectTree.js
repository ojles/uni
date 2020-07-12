import React from 'react';
import {Treebeard} from 'react-treebeard';
import DefaultApi from '../../api/index';
import {Api} from '../../api/index';
import ObjectTreeStyle from './ObjectTreeStyle'
import {connect} from 'react-redux'

import './ObjectTree.css'

class ObjectTree extends React.Component {
    componentDidMount() {
        DefaultApi.getObjects()
            .then(objects => {
                objects.forEach(object => {
                    object.sourceUrl = DefaultApi.apiUrl;
                });
                this.props.initTreeData(objects, DefaultApi.apiUrl);
            });
    }

    onToggle = (node, toggled) => {
        if (!toggled) {
            this.props.toggleTreeNodeAndSetChildren(node);
            return;
        }

        if (node.sourceUrl && node.clazz === 'LINK') {
            let api = new Api(node.sourceUrl);
            api.getObjectById(node.id)
                .then(object => {
                    object.sourceUrl = node.sourceUrl;
                    this.props.changeCurrentObject(object);
                    new Api(object.url).getObjects()
                        .then(children => {
                            for (let i = 0; i < children.length; i++) {
                                children[i].sourceUrl = object.url;
                            }
                            this.props.toggleTreeNodeAndSetChildren(node, children);
                        });
                });
        } else if (node.sourceUrl) {
            let api = new Api(node.sourceUrl);
            api.getObjectById(node.id)
                .then(object => {
                    object.sourceUrl = node.sourceUrl;
                    this.props.changeCurrentObject(object);
                });
            api.getObjects(node.id)
                .then(children => {
                    for (let i = 0; i < children.length; i++) {
                        children[i].sourceUrl = node.sourceUrl;
                    }
                    this.props.toggleTreeNodeAndSetChildren(node, children);
                });
        } else {
            console.error('Invalid node without sourceUrl: ', node);
        }
    }

    render() {
        return (
            <div className="uni-object-tree-wrapper">
                <Treebeard data={this.props.data} onToggle={this.onToggle} style={ObjectTreeStyle}/>
            </div>
        );
    }
}

const mapStateToProps = (state, ownProps) => {
    return {
        data: {
            ...state.objectTree.data
        }
    };
}

const mapDispatchToProps = (dispatch) => {
    return {
        initTreeData: (objects, sourceUrl) => {
            dispatch({
                type: 'INIT_TREE_DATA',
                payload: {
                    objects,
                    sourceUrl
                }
            });
        },
        changeCurrentObject: (object)  => {
            dispatch({
                type: 'CHANGE_CURRENT_OBJECT',
                payload: object
            });
        },
        toggleTreeNodeAndSetChildren: (node, children) => {
            dispatch({
                type: 'TOGGLE_TREE_NODE_AND_SET_CHILDREN',
                payload: {
                    node,
                    children
                }
            });
        }
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(ObjectTree);
