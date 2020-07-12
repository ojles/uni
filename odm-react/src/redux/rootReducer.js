import {combineReducers} from 'redux'
import objectReducer from './objectReducer'
import newObjectReducer from './newObjectReducer'
import objectTreeReducer from './objectTreeReducer'

const rootReducer = combineReducers({
    object: objectReducer,
    newObject: newObjectReducer,
    objectTree: objectTreeReducer
});

export default rootReducer;
