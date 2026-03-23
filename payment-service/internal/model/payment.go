package model

import "time"

type PaymentStatus string


const (
	StatusPending 			PaymentStatus = "PENDING"
	StatusPaid 				PaymentStatus = "PAID"
	StatusFailed 			PaymentStatus = "FAILED"
	StatusRefunded 			PaymentStatus = "REFUNDED"
	StatusPertiallyRefunded PaymentStatus = "PERTIALLY_REFUNDED"
)


type Payment struct {
	ID 			string 			`json:"id"`
	OrderID 	string 			`json:"order_id"`
	BuyerID 		string 			`json:"user_id"`
	Amount 		string 			`json:"amount"`
	Provider 	string 			`json:"porvider"`
	Status 		PaymentStatus 	`json:"status"`
	CreatedAt 	time.Time 		`json:"created_at"`
	UpdatedAt 	time.Time 		`json:"updated_at"`
}