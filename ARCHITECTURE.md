# Roamwise architecture

```mermaid
flowchart LR
    U[Traveler] --> T[Travel Coordinator]
    T --> H[Local Hike Agent]
    T --> N[National Park Agent]
    T --> F[Food Agent]
    T --> B[Booking Agent]
    T --> G[Gas Price Agent]
    T --> V[Vision Agent]
    T --> X[Voice Translation Agent]
    H --> P[Trail & weather providers]
    N --> NP[National Park data]
    F --> Y[Yelp MCP / reviews]
    B --> BK[Travel & reservation providers]
    G --> GP[Gas-price provider]
    V --> VM[Vision model]
    X --> TM[Speech + translation provider]
    H --> T
    N --> T
    F --> T
    B --> T
    G --> T
    T --> M[(Preference + feedback memory)]
    M --> T
```

The coordinator delegates independent searches, ranks results against the
traveler profile and recent activities, and asks for explicit confirmation
before any reservation or purchase.
