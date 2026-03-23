package handler

import (
	"encoding/json"
	"net/http"
	"payment-service/internal/dto"
	"payment-service/internal/model"
	"payment-service/internal/repository"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgxpool"
)


func CreatePaymentHandler(pool *pgxpool.Pool) http.Handler {
	repo := repository.NewPaymentRepository(pool)

	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request){
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return 
		}

		var req dto.OrderCreatedEvent
		if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
			http.Error(w, "Invalid body", http.StatusBadRequest)
			return
		}

		now := time.Now()

		payment := model.Payment{
			ID: 		uuid.NewString(),
			OrderID: 	req.OrderID,
			BuyerID: 	req.BuyerID,
			Amount: 	req.Amount,
			Provider: 	req.Provider,
			Status: 	model.StatusPending,
			CreatedAt: 	now,
			UpdatedAt: 	now,
		}

		if err := repo.Create(r.Context(), &payment); err != nil {
			http.Error(w, "db.error", http.StatusInternalServerError)
			return
		}

		w.WriteHeader(http.StatusCreated)
		
	})

}