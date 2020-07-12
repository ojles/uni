# Load Balancing

A simple load balancing example using rabbitmq.
The [compute](compute) instances get tasks from the queue.
Each instance can process one task at a time (you can change this value in [ApplicationConfiguration.java](compute/src/main/java/ojles/loadbalancing/compute/config/ApplicationConfiguration.java#L43).

For detailed instructions how to start the project go to [deploy-scripts](deploy-scripts)
