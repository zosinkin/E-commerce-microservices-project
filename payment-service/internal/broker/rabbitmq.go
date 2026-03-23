package rabbitmq


import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)


type RabbitMQClient struct {
	conn 		*amqp.Connection
	channel 	*amqp.Channel
	exchange 	string
}


func NewRabbitMQClient(url string, exchange string) (*RabbitMQClient, error) {
	conn, err := amqp.Dial(url)
	if err != nil {
		return nil, fmt.Errorf("RabbitMQ dial error: %w", err)
	}

	ch, err := conn.Channel()
	if err != nil {
		return nil, fmt.Errorf("RabbitMQ channel error: %w", err)
	}

	err = ch.ExchangeDeclare(
		exchange,
		"topic",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		_ = ch.Close()
		_ = conn.Close()
		return nil, fmt.Errorf("Exchange declare error: %w", err)
	}

	return &RabbitMQClient{
		conn: 		conn,
		channel: 	ch,
		exchange: 	exchange,
	}, nil
}


func (r *RabbitMQClient) Publish(routingKey string, message any) error {
	body, err := json.Marshal(message)
	if err != nil {
		return fmt.Errorf("json marshal error: %w", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	err = r.channel.PublishWithContext(
		ctx,
		r.exchange,
		routingKey,
		false,
		false,
		amqp.Publishing{
			ContentType: 	"application/json",
			DeliveryMode: 	amqp.Persistent,
			Body: 			body,
			Timestamp: 		time.Now(),
		},
	)
	if err != nil {
		return fmt.Errorf("publish error: %w", err)
	}
	return nil
}


func (r *RabbitMQClient) Consume(queueName string, routingKey string, handler func([]byte) error) error {
	_, err := r.channel.QueueDeclare(
		queueName,
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return fmt.Errorf("Queue bind error: %w", err)
	}

	err = r.channel.QueueBind(
		queueName,
		routingKey,
		r.exchange,
		false,
		nil,
	)
	if err != nil {
		return fmt.Errorf("qos error: %w", err)
	}

	err = r.channel.Qos(
		10,
		0,
		false,
	)
	if err != nil {
		return fmt.Errorf("qos error: %w", err)
	}

	msgs, err := r.channel.Consume(
		queueName,
		"",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		return fmt.Errorf("consume error: %w", err)
	}

	go func() {
		for msg := range msgs {
			fmt.Printf("Message body: %s", msg.Body)
			if err := handler(msg.Body); err != nil {
				log.Printf("consume handler error: %v", err)
				_ = msg.Nack(false, true)
				continue
			}

			_ = msg.Ack(false)
		}
	}()
	return nil
}


func (r *RabbitMQClient) Close() error {
	if r.channel != nil {
		_ = r.channel.Close()
	}
	if r.conn != nil {
		_ = r.conn.Close()
	}
	return nil
}
