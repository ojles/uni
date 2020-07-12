package ojles.loadbalancing.compute.config;

import ojles.loadbalancing.compute.service.TaskMessageListener;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.TopicExchange;
import org.springframework.amqp.rabbit.connection.ConnectionFactory;
import org.springframework.amqp.rabbit.listener.SimpleMessageListenerContainer;
import org.springframework.amqp.rabbit.listener.adapter.MessageListenerAdapter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableScheduling;

@Configuration
@EnableScheduling
public class ApplicationConfiguration {
    @Bean
    Queue queue() {
        return new Queue("tasks", false);
    }

    @Bean
    TopicExchange exchange() {
        return new TopicExchange("tasks-exchange");
    }

    @Bean
    Binding binding(Queue queue, TopicExchange exchange) {
        return BindingBuilder
                .bind(queue)
                .to(exchange)
                .with("tasks");
    }

    @Bean
    SimpleMessageListenerContainer container(ConnectionFactory connectionFactory,
                                             MessageListenerAdapter listenerAdapter) {
        SimpleMessageListenerContainer container = new SimpleMessageListenerContainer();
        container.setConnectionFactory(connectionFactory);
        container.setQueueNames("tasks");
        container.setMessageListener(listenerAdapter);
        container.setConcurrentConsumers(1);
        return container;
    }

    @Bean
    MessageListenerAdapter listenerAdapter(TaskMessageListener receiver) {
        return new MessageListenerAdapter(receiver, "receiveMessage");
    }
}
