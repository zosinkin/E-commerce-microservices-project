package service

import (
	"context"
	"log"
	"time"

	"payment-service/internal/dto"
	"payment-service/internal/model"
	"payment-service/internal/repository"

	"github.com/google/uuid"
)


type PaymentRepository interface {
	Create(ctx context.Context, p *model.Payment) error
}


type PaymentService struct {
	repo PaymentRepository
}


func NewPaymentService(repo PaymentRepository) *PaymentService {
	return &PaymentService{repo: repo}
}


func (s *PaymentService) CreateFromOrderEvent(ctx context.Context, event dto.OrderCreatedEvent) (*model.Payment, error) {
	now := time.Now()

	payment := &model.Payment{
		ID: 		uuid.NewString(),
		OrderID: 	event.OrderID,
		BuyerID: 	event.BuyerID,
		Amount: 	event.Amount,
		Provider: 	"mock",
		Status: 	model.StatusPending,
		CreatedAt: 	now,
		UpdatedAt: 	now,
	}
	if err := s.repo.Create(ctx, payment); err != nil {
		return nil, err
	}
	log.Println("The data has been successfully added to the database.")
	return payment, nil
}

var _ PaymentRepository = (*repository.PaymentRepository)(nil)