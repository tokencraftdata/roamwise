"""Roamwise multi-agent travel coordinator (Python 3.11+).

Live providers implement the small Protocol interfaces below. The Yelp adapter
is intentionally dependency-injected so credentials never enter prompts.
"""
from dataclasses import dataclass, field
from typing import Protocol, Literal

Intent = Literal["local_hike", "national_park", "us_trip", "food", "menu", "booking", "gas", "voice", "vision"]

@dataclass
class TravelerProfile:
    home: str
    diet: list[str] = field(default_factory=list)
    trail_level: str = "moderate"
    budget: str = "mid-range"
    disliked: list[str] = field(default_factory=list)
    recent: list[str] = field(default_factory=list)

class Provider(Protocol):
    def search(self, query: str, location: str, profile: TravelerProfile) -> list[dict]: ...

class Specialist:
    def __init__(self, name: str, provider: Provider):
        self.name, self.provider = name, provider

    def run(self, query: str, location: str, profile: TravelerProfile) -> list[dict]:
        return self.provider.search(query, location, profile)

class TravelCoordinator:
    """Routes requests and combines specialists; bookings require confirmation."""
    def __init__(self, agents: dict[Intent, Specialist]):
        self.agents = agents

    def plan(self, request: dict, profile: TravelerProfile) -> dict:
        intents: list[Intent] = request.get("intents", ["us_trip", "food"])
        results = {kind: self.agents[kind].run(request["query"], request["location"], profile)
                   for kind in intents if kind in self.agents}
        return {"profile_used": profile, "specialists": results,
                "requires_confirmation": "booking" in intents}

class MenuReviewAgent(Specialist):
    """Ranks local restaurants using dish-level review evidence, not stars alone."""
    def rank_menu(self, restaurant: dict, profile: TravelerProfile) -> dict:
        menu = restaurant.get("menu", [])
        repeat_local_praise = restaurant.get("review_signals", {}).get("repeat_local_praise", 0)
        dish_fit = sum(1 for dish in menu if not set(dish.get("tags", [])) & set(profile.disliked))
        return {**restaurant, "menu_match": round(0.65 * dish_fit / max(len(menu), 1)
                                                   + 0.35 * repeat_local_praise, 2)}

class TranslationAgent(Specialist):
    """Accepts speech transcripts and returns text plus speakable translation."""

class VisionAgent(Specialist):
    """Explains an uploaded landmark, menu, sign, plant, or trail image."""

# Example wiring:
# agents = {"food": Specialist("Food agent", YelpProvider(mcp_client)), ...}
# plan = TravelCoordinator(agents).plan(request, traveler_profile)
