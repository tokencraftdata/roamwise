# Roamwise

Personalized multi-agent travel planning for local hikes, national parks,
U.S. trips, restaurants, bookings, and fuel stops.

## Run the interface

```bash
npm install
npm run dev
```

## Python coordinator

[`agent.py`](agent.py) contains the provider-neutral Python orchestration layer.
Implement the `Provider` protocol for Yelp MCP, trail data, booking inventory,
and gas prices, then inject those specialists into `TravelCoordinator`.

The system never completes a purchase without explicit user confirmation.
See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the agent diagram.

## Integration status

- Yelp MCP: adapter boundary ready; live connector and credentials required.
- Booking/prices: confirmation flow ready; live provider required.
- Preference loop: device-local prototype storage in the web interface.
