from experta import Fact, Field


class Question(Fact):
    pass


class Answer(Fact):
    pass


class Cracked(Fact):
    size = Field(float, mandatory=True)


class Burned(Fact):
    percentage = Field(float, mandatory=True)


class UnderCooked(Fact):
    percentage = Field(float, mandatory=True)


class OverSized(Fact):
    size = Field(float, mandatory=True)


class UnderSized(Fact):
    size = Field(float, mandatory=True)


class Contaminated(Fact):
    pass
