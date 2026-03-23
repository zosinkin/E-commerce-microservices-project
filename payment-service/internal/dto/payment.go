package dto


type PaymentCreatedEvent struct {
	Event     string `json:"event"`
	PaymentID string `json:"payment_id"`
	OrderID   string `json:"order_id"`
	UserID    string `json:"user_id"`
	Amount    string `json:"amount"`
	Provider  string `json:"provider"`
	Status    string `json:"status"`
}


type OrderCreatedEvent struct {
	Event     	string `json:"event"`
	PaymentID 	string `json:"payment_id"`
	OrderID   	string `json:"order_id"`
	BuyerID    	string `json:"buyer_id"`
	Amount    	string `json:"amount"`
	Provider  	string `json:"provider"`
	Status    	string `json:"status"`
}

