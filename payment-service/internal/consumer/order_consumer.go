package consumer


import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	rabbitmq "payment-service/internal/broker"
	"payment-service/internal/dto"
	"payment-service/internal/service"
)


type OrderConsumer struct {
	paymentService *service.PaymentService
	rabbit *rabbitmq.RabbitMQClient
}


func  NewOrderConsumer(paymentService *service.PaymentService, rabbitClient *rabbitmq.RabbitMQClient) *OrderConsumer {
	return &OrderConsumer{
		paymentService: paymentService,
		rabbit: 	rabbitClient,
	}
}


func (c *OrderConsumer) HandleOrderCreated(body []byte) error {
	var event dto.OrderCreatedEvent
	if err := json.Unmarshal(body, &event); err != nil {
		return fmt.Errorf("unmarshal order.create order: %w", err)
	}

	log.Printf("received order.created event: order_id=%s buyer_id=%s", event.OrderID, event.BuyerID)

	payment, err := c.paymentService.CreateFromOrderEvent(context.Background(), event)
	if err != nil {
		return fmt.Errorf("Create payment from event error: %w", err)
	}

	outEvent := dto.PaymentCreatedEvent{
		Event: "payment.created",
		PaymentID: payment.ID,
		OrderID: payment.OrderID,
		UserID: payment.BuyerID,
		Amount: payment.Amount,
		Provider: payment.Provider,
		Status: string(payment.Status),
	}

	if err := c.rabbit.Publish("payment.created", outEvent); err != nil {
		return fmt.Errorf("publish payment.created error: %w", err)
	}

	log.Printf("payment created and published: payment_id=%s order_id=%s", payment.ID, payment.OrderID)

	return nil
}