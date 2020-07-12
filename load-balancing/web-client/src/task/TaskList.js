import React, {Component} from 'react';
import ReactCSSTransitionGroup from 'react-addons-css-transition-group'; // ES6
import {getAllTasks} from '../util/APIUtils';
import Task from './Task';
import LoadingIndicator from '../common/LoadingIndicator';
import {withRouter} from 'react-router-dom';
import './TaskList.css';

class TaskList extends Component {
    constructor(props) {
        super(props);
        this.state = {
            tasks: [],
            isLoading: false
        };
        this.taskRefreshInterval = null;
    }

    refreshTaskList = () => {
        let promise = getAllTasks();
        if (!promise) {
            return;
        }
        promise
            .then(response => {
                this.setState({
                    tasks: response.filter(task => (task.progress / task.executionSeconds) !== 1)
                })
            })
    }

    componentDidMount() {
        this.refreshTaskList();
        clearInterval(this.taskRefreshInterval);
        this.taskRefreshInterval = setInterval(this.refreshTaskList, 1500);
    }

    componentWillUnmount() {
        clearInterval(this.taskRefreshInterval);
    }

    render() {
        const tasksView = [];
        this.state.tasks.forEach(task => {
            tasksView.push(<Task key={task.id}
                              id={task.id}
                              progress={task.progress}
                              executionSeconds={task.executionSeconds}
                              instanceName={task.instanceName}/>)
        });

        return (
            <div className="polls-container">
                <ReactCSSTransitionGroup transitionName="example"
                    transitionEnterTimeout={500}
                    transitionLeaveTimeout={600}>
                    {tasksView}
                </ReactCSSTransitionGroup>
                {
                    !this.state.isLoading && this.state.tasks.length === 0 ? (
                        <div className="no-polls-found">
                            <span>No Tasks Found.</span>
                        </div>
                    ) : null
                }
                {
                    this.state.isLoading ?
                        <LoadingIndicator/> : null
                }
            </div>
        );
    }
}

export default withRouter(TaskList);
