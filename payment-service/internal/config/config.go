package config

import (
	"os"
	"log"
	"github.com/joho/godotenv"
)


type Config struct {
	DatabaseUrl string
	RabbitMqUrl string
}


func Load() *Config {
	err := godotenv.Load("./.env")
	if err != nil {
		log.Fatalf("Failed to load .env from parent directory: %v", err)
	}
	return &Config{
		DatabaseUrl: os.Getenv("DATABASE_URL"),
		RabbitMqUrl: os.Getenv("RABBITMQ_URL"),
	}
}