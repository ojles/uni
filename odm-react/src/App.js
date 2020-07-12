import React from 'react';
import './App.css';
import {BrowserRouter} from 'react-router-dom';
import TreeSplitView from './components/TreeSplitView'
import store from './redux/store'
import {Provider} from 'react-redux'

const App = (props) => {
    return (
        <Provider store={store}>
            <div className="App">
                <BrowserRouter>
                    <TreeSplitView/>
                </BrowserRouter>
            </div>
        </Provider>
    );
}

export default App;
