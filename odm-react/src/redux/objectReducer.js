const initState = {
    id: 0,
    name: ''
};

const objectReducer = (state = initState, action) => {
    if (action.type === 'UPDATE_OBJECT_DATA') {
        return action.payload;
    }

    if (action.type === 'CHANGE_CURRENT_OBJECT') {
        return action.payload;
    }

    if (action.type === 'UPDATE_OBJECT_PROPERTY') {
        const {id, newValue} = action.payload;
        return {
            ...state,
            [id]: newValue
        };
    }

    if (action.type === 'REMOVE_OBJECT') {
        return action.payload.majorObject;
    }

    return state;
}

export default objectReducer;
