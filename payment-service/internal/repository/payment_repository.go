package repository

import (
	"context"
	"payment-service/internal/model"

	"github.com/jackc/pgx/v5/pgxpool"
)

type Payment interface {
	Create()
}

type PaymentRepository struct {
	pool *pgxpool.Pool
}


func NewPaymentRepository(pool *pgxpool.Pool) *PaymentRepository {
	return &PaymentRepository{pool: pool}
}


func (r *PaymentRepository) Create(ctx context.Context, p *model.Payment) error {
	query := `
		INSERT INTO payments (id, order_id, userr_id, amount, porvider, status, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
	`
	_, err := r.pool.Exec(ctx, query,
		p.ID,
		p.OrderID,
		p.BuyerID,
		p.Amount,
		p.Provider,
		p.Status,
		p.CreatedAt,
		p.UpdatedAt,
	)
	return err
}
