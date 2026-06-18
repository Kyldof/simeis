FROM rust:1.88.0-bookworm AS builder

WORKDIR /app

COPY . .

RUN cargo build --release -p simeis-server

FROM debian:bookworm-slim

WORKDIR /app

COPY --from=builder /app/target/release/simeis-server .

EXPOSE 8080

CMD ["./simeis-server"]
