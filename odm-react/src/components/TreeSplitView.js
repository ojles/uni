import React from 'react';
import ObjectTree from './tree/ObjectTree'
import SplitPane from 'react-split-pane'
import TreeSplitElement from './TreeSplitElement'

import './TreeSplitView.css'

const TreeSplitView = (props) => {
    return (
         <SplitPane split="vertical" minSize={150} defaultSize={360}>
	     <ObjectTree/>
             <TreeSplitElement/>
         </SplitPane>
    );
}

export default TreeSplitView;
