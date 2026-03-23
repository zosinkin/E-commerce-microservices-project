package app

import (
	"log"
	"net/http"
	"payment-service/internal/broker"
	"payment-service/internal/config"
	"payment-service/internal/consumer"
	"payment-service/internal/db"
	"payment-service/internal/handler"
	"payment-service/internal/repository"
	"payment-service/internal/service"
)

func Run() error {
	cfg := config.Load()
	pool := db.NewPostgresPool(cfg.DatabaseUrl)

	mux := http.NewServeMux()
	rabbit, err := rabbitmq.NewRabbitMQClient(cfg.RabbitMqUrl, "events")
	if err != nil {
		return err
	}
	defer rabbit.Close()

	paymentRepo := repository.NewPaymentRepository(pool)
	paymentService := service.NewPaymentService(paymentRepo)
	orderConsumer := consumer.NewOrderConsumer(paymentService, rabbit)

	err = rabbit.Consume(
		"order.created.payment",
		"order.created",
		orderConsumer.HandleOrderCreated,
	)
	if err != nil {
		return nil
	}

	
	mux.HandleFunc("/health", handler.HealthHandler)
	mux.Handle("/payments", handler.CreatePaymentHandler(pool))

	addr := ":8080"
	log.Printf("payment-service started on %s", addr)

	return http.ListenAndServe(addr, mux)
}