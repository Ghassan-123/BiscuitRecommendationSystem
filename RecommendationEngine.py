from experta import *
from MyFacts import *


class RecommendationEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []

    @DefFacts()
    def _initial_facts(self):
        yield Fact(init=True)  # Simple initialization fact

    # Cracked rules
    @Rule(Cracked(size=P(lambda x: x >= 20)))
    def critical_cracked(self):
        self.declare(
            Fact(recommendation="Reject entire batch - critical cracking (≥20%)")
        )

    @Rule(Cracked(size=P(lambda x: 5 <= x < 20)))
    def moderate_cracked(self):
        self.declare(
            Fact(recommendation="Sort and remove cracked items (5-20% cracked)")
        )

    @Rule(Cracked(size=P(lambda x: x < 5)))
    def minor_cracked(self):
        self.declare(Fact(recommendation="Monitor cracking (≤5%) - normal wear"))

    # Burned rules
    @Rule(Burned(percentage=P(lambda x: x >= 15)))
    def critical_burned(self):
        self.declare(
            Fact(recommendation="Adjust heating process and reject batch (≥15% burned)")
        )

    @Rule(Burned(percentage=P(lambda x: 3 <= x < 15)))
    def moderate_burned(self):
        self.declare(Fact(recommendation="Inspect heating equipment (3-15% burned)"))

    # UnderCooked rules
    @Rule(UnderCooked(percentage=P(lambda x: x >= 10)))
    def critical_undercooked(self):
        self.declare(
            Fact(recommendation="Increase cooking time/temperature (≥10% undercooked)")
        )

    @Rule(UnderCooked(percentage=P(lambda x: x < 10)))
    def acceptable_undercooked(self):
        self.declare(
            Fact(recommendation="Minor undercooking (≤10%) - within tolerance")
        )

    # Size-related rules
    @Rule(OverSized(size=P(lambda x: x >= 15)))
    def critical_oversized(self):
        self.declare(
            Fact(recommendation="Major oversizing (≥15%) - recalibrate equipment")
        )

    @Rule(OverSized(size=P(lambda x: 5 <= x < 15)))
    def moderate_oversized(self):
        self.declare(Fact(recommendation="Check sizing equipment (5-15% oversized)"))

    @Rule(UnderSized(size=P(lambda x: x >= 15)))
    def critical_undersized(self):
        self.declare(
            Fact(recommendation="Major undersizing (≥15%) - recalibrate equipment")
        )

    @Rule(UnderSized(size=P(lambda x: 5 <= x < 15)))
    def moderate_undersized(self):
        self.declare(Fact(recommendation="Check sizing equipment (5-15% undersized)"))

    # Contamination rule
    @Rule(Contaminated(), salience=1000)
    def force_reject(self):
        self.declare(Fact(recommendation="CRITICAL: Foreign object found in dough"))

    # Collect recommendations
    @Rule(Fact(recommendation=MATCH.r), salience=-1000)
    def collect_recommendation(self, r):
        if r not in self.recommendations:
            self.recommendations.append(r)
