import React from 'react';
import './Task.css';

const Task = (props) => {
    const executionPercentage = Math.round((props.progress / props.executionSeconds) * 100);
    return (
        <div className="poll-content">
            <div className="poll-header">
                <div className="poll-question">
                    {'Task #' + props.id + ' (' + props.instanceName + ')'}
                </div>
            </div>
            <div className="poll-choices">
                <div className="cv-poll-choice">
                    <span className="cv-poll-choice-details">
                        <span className="cv-choice-percentage">
                            {executionPercentage}%
                        </span>
                    </span>
                    <span className={'cv-choice-percent-chart'}
                          style={{width: executionPercentage + '%'}}>
                    </span>
                </div>
                <span>Time: {props.executionSeconds} seconds</span><br/>
                <span>Progress: {props.progress} seconds</span>
            </div>
        </div>
    );
};


export default Task;
