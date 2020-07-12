import React, {Component} from 'react';
import {createTask} from '../util/APIUtils';
import './NewTask.css';
import {Button, Form, Input, notification} from 'antd';

const FormItem = Form.Item;

class NewTask extends Component {
    constructor(props) {
        super(props);
        this.state = {
            taskDuration: null
        };
    }

    handleSubmit = (event) => {
        event.preventDefault();
        const task = {
            executionSeconds: parseInt(this.state.taskDuration)
        };

        console.log('Creating task: ', task);
        createTask(task)
            .then(response => {
                this.props.history.push("/");
            }).catch(error => {
            if (error.status === 401) {
                this.props.handleLogout('/login', 'error', 'You have been logged out. Please login create poll.');
            } else {
                notification.error({
                    message: 'Load Balancing',
                    description: error.message || 'Sorry! Something went wrong. Please try again!'
                });
            }
        });
    };

    isFormInvalid = () => {
        return this.state.taskDuration === null || this.state.taskDuration === '';
    };

    handleTaskDurationChange = (event) => {
        this.setState({
            taskDuration: event.target.value
        })
        // implement
    };

    render() {
        return (
            <div className="new-poll-container">
                <h1 className="page-title">Create Task</h1>
                <div className="new-poll-content">
                    <Form onSubmit={this.handleSubmit} className="create-poll-form">
                        <FormItem className="poll-form-row">
                            <Input placeholder="Task duration in seconds"
                                   size="large"
                                   value={this.state.taskDuration}
                                   onChange={this.handleTaskDurationChange}/>
                        </FormItem>
                        <FormItem className="poll-form-row">
                            <Button type="primary"
                                    htmlType="submit"
                                    size="large"
                                    disabled={this.isFormInvalid()}
                                    className="create-poll-form-button">
                                Create Task
                            </Button>
                        </FormItem>
                    </Form>
                </div>
            </div>
        );
    }
}

export default NewTask;
