package db


import (
	"context"
	"log"
	"github.com/jackc/pgx/v5/pgxpool"
)


func NewPostgresPool(databaseURL string) *pgxpool.Pool {
	pool, err := pgxpool.New(context.Background(), databaseURL)
	if err != nil {
		log.Fatal("cannot connect to db:", err)
	}

	return pool
}