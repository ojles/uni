const initState = {
    data: {
        id: 0,
        name: 'University',
        children: []
    }
};

const _recursiveObjectSearch = (startNode, id, sourceUrl, objects) => {
    if (startNode.id === id && startNode.sourceUrl === sourceUrl) {
        objects.push(startNode);
    }

    if (startNode.children !== null) {
        for (let i = 0; i < startNode.children.length; i++) {
            _recursiveObjectSearch(startNode.children[i], id, sourceUrl, objects);
        }
    }
};

const findObjectByIdAndUrl = (startNode, id, sourceUrl) => {
    let objects = [];
    _recursiveObjectSearch(startNode, id, sourceUrl, objects);
    return objects;
};

// TODO: rewrite this
const removeNodeByIdAndUrl = (startNode, id, sourceUrl) => {
    if (!startNode.children) {
        return;
    }

    for (let i = 0; i < startNode.children.length; i++) {
        if (startNode.children[i].id === id && startNode.children[i].sourceUrl === sourceUrl) {
            startNode.children.splice(i, 1);
            return;
        }
    }

    for (let i = 0; i < startNode.children.length; i++) {
        removeNodeByIdAndUrl(startNode.children[i], id, sourceUrl);
    }
};

const objectTreeReducer = (state = initState, action) => {
    if (action.type === 'UPDATE_OBJECT_DATA') {
        const newObject = action.payload;
        if (newObject.clazz === 'LINK') {
            findObjectByIdAndUrl(state.data, newObject.id, newObject.sourceUrl)
                .forEach(node => {
                    node.children = [];
                    node.toggled = false;
                    node.name = newObject.name;
                });
        } else {
            findObjectByIdAndUrl(state.data, newObject.id, newObject.sourceUrl)
                .forEach(node => {
                    node.name = newObject.name;
                });
        }
        return {...state};
    }

    if (action.type === 'ADD_NEW_OBJECT') {
        const newObject = action.payload.newObject;
        findObjectByIdAndUrl(state.data, newObject.majorId, newObject.sourceUrl)
            .forEach(parentNode => {
                parentNode.children.push({
                    ...action.payload.newObject,
                    children: []
                });
            });
        return {...state};
    }

    if (action.type === 'REMOVE_OBJECT') {
        const nextState = {...state};
        const {id, sourceUrl} = action.payload.object;
        removeNodeByIdAndUrl(nextState.data, id, sourceUrl);
        return nextState;
    }

    if (action.type === 'INIT_TREE_DATA') {
        const {objects, sourceUrl} = action.payload;
        for (let i = 0; i < objects.length; i++) {
            objects[i].children = [];
        }
        return {
            data: {
                ...state.data,
                toggled: true,
                children: objects,
                sourceUrl
            }
        }
    }

    if (action.type === 'UPDATE_TREE_DATA') {
        return {
            data: action.payload.data
        };
    }

    if (action.type === 'TOGGLE_TREE_NODE_AND_SET_CHILDREN') {
        const {node, children} = action.payload;
        node.toggled = !node.toggled;
        if (node.toggled) {
            node.children = children;
            for (let i = 0; i < children.length; i++) {
                children[i].children = [];
            }
        } else {
            node.children = [];
        }

        // because we don't make a deep copy of the object tree
        // we change the clicked 'node' directly.
        return {...state};
    }

    return state;
}

export default objectTreeReducer;
