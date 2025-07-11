from experta import *
from MyFacts import *


class RecommendationEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.recommendations = []

    @DefFacts()
    def _initial_facts(self):
        yield Fact(init=True)  # Simple initialization fact
        yield Question(
            id="total",
            Type="input",
            valid=[],
            text="What is the batch size?",
        )
        yield Question(
            id="deffected",
            Type="input",
            valid=[],
            text="how many biscuits are deffected?",
        )
        yield Question(
            id="cracked",
            Type="input",
            valid=[],
            text="how many biscuits are cracked?",
        )
        yield Question(
            id="burned",
            Type="input",
            valid=[],
            text="how many biscuits are burned?",
        )
        yield Question(
            id="under_cooked",
            Type="input",
            valid=[],
            text="how many biscuits are under_cooked?",
        )
        yield Question(
            id="over_sized",
            Type="input",
            valid=[],
            text="how many biscuits are over_sized?",
        )
        yield Question(
            id="under_sized",
            Type="input",
            valid=[],
            text="how many biscuits are under_sized?",
        )
        yield Question(
            id="contaminated",
            Type="input",
            valid=[],
            text="how many biscuits are contaminated?",
        )
        yield Question(
            id="cracked_size",
            Type="input",
            valid=[],
            text="what is the average crack rate(example: 50%, 30%, etc...)?",
        )
        yield Question(
            id="burned_percentage",
            Type="input",
            valid=[],
            text="what is the average burn rate(example: 50%, 30%, etc...)?",
        )
        yield Question(
            id="under_cooked_percentage",
            Type="input",
            valid=[],
            text="what is the average under_cooked rate(example: 50%, 30%, etc...)?",
        )
        yield Question(
            id="over_sized_size",
            Type="input",
            valid=[],
            text="what is the average size(radius) of the biscuits(example: 4cm, 10cm, etc...)?",
        )

    @Rule(
        Question(id=MATCH.id, text=MATCH.text, valid=MATCH.valid, Type=MATCH.Type),
        NOT(Answer(id=MATCH.id)),
        AS.ask << Fact(ask=MATCH.id),
    )
    def ask_question_by_id(self, ask, id, text, valid, Type):
        # "Ask a question and assert the answer""
        self.retract(ask)
        answer = self.ask_user(text, Type, valid)
        answer = answer.strip().replace("%", "")
        self.declare(Answer(id=id, text=answer))

    # Useful functions
    def ask_user(self, question, Type, valid=None):
        # "Ask a question, and return the answer"
        answer = ""
        while not (self.is_of_type(answer, Type, valid)):
            print(question)
            answer = input()
        return answer

    def is_of_type(self, answer, Type, valid):
        # "Check that the answer has the right form"
        if Type == "input":
            ans = answer.strip().replace("%", "")
            return self.is_a_number(ans)
        else:
            pass

    def is_a_number(self, answer):
        try:
            int(answer)
            if answer > 0:
                return True
            else:
                return False
        except:
            return False

    # Input validation rules

    @Rule(NOT(Answer(id=L("total"))), NOT(Fact(ask=L("total"))))
    def supply_answer_total(self):
        self.declare(Fact(ask="total"))

    @Rule(
        (Answer(id=L("total"))),
        NOT(Answer(id=L("deffected"))),
    )
    def supply_answer_deffected(self):
        self.declare(Fact(ask="deffected"))

    @Rule(
        AS.Def << Answer(id=L("deffected"), text=MATCH.ans1),
        Answer(id=L("total"), text=MATCH.ans2),
        TEST(lambda ans1, ans2: int(ans1) > int(ans2)),
        salience=50,
    )
    def validation1(self, Def):
        self.retract(Def)
        self.declare(Fact(ask="deffected"))

    @Rule(
        (Answer(id=L("deffected"))),
        NOT(Answer(id=L("cracked"))),
    )
    def supply_answer_cracked(self):
        self.declare(Fact(ask="cracked"))

    @Rule(
        (Answer(id=L("cracked"))),
        NOT(Answer(id=L("burned"))),
    )
    def supply_answer_burned(self):
        self.declare(Fact(ask="burned"))

    @Rule(
        (Answer(id=L("burned"))),
        NOT(Answer(id=L("under_cooked"))),
    )
    def supply_answer_under_cooked(self):
        self.declare(Fact(ask="under_cooked"))

    @Rule(
        (Answer(id=L("under_cooked"))),
        NOT(Answer(id=L("over_sized"))),
    )
    def supply_answer_over_sized(self):
        self.declare(Fact(ask="over_sized"))

    @Rule(
        (Answer(id=L("over_sized"))),
        NOT(Answer(id=L("under_sized"))),
    )
    def supply_answer_under_sized(self):
        self.declare(Fact(ask="under_sized"))

    @Rule(
        (Answer(id=L("under_sized"))),
        NOT(Answer(id=L("contaminated"))),
    )
    def supply_answer_contaminated(self):
        self.declare(Fact(ask="contaminated"))

    @Rule(
        Answer(id=L("deffected"), text=MATCH.ans1),
        AS.cr << Answer(id=L("cracked"), text=MATCH.ans2),
        AS.bu << Answer(id=L("burned"), text=MATCH.ans3),
        AS.unc << Answer(id=L("under_cooked"), text=MATCH.ans4),
        AS.ovs << Answer(id=L("over_sized"), text=MATCH.ans5),
        AS.uns << Answer(id=L("under_sized"), text=MATCH.ans6),
        AS.co << Answer(id=L("contaminated"), text=MATCH.ans7),
        TEST(
            lambda ans1, ans2, ans3, ans4, ans5, ans6, ans7: int(ans1)
            < int(ans2 + ans3 + ans4 + ans5 + ans6 + ans7)
        ),
        salience=50,
    )
    def validation2(self, cr, bu, unc, ovs, uns, co):
        self.retract(cr)
        self.retract(bu)
        self.retract(unc)
        self.retract(ovs)
        self.retract(uns)
        self.retract(co)
        self.declare(Fact(ask="cracked"))

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
