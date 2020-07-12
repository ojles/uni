const initState = {
    id: 0,
    name: ''
};

const newObjectReducer = (state = initState, action) => {
    if (action.type === 'UPDATE_NEW_OBJECT_PROPERTY') {
        const {id, newValue} = action.payload;
        return {
            ...state,
            [id]: newValue
        };
    }

    if (action.type === 'ADD_NEW_OBJECT') {
        return {
            id: 0,
            name: ''
        };
    }

    return state;
}

export default newObjectReducer;
