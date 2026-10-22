dev:
	(cd backend && ADMIN_TOKEN=dev go run ./cmd/server) & \
	(cd frontend && npm run dev)

build:
	cd frontend && npm run build
	cd backend && go build -o ../kiosk ./cmd/server
