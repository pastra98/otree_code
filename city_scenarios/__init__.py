from otree.api import *
from otree.forms.widgets import RadioSelect

# TODO:


doc = """
Testing the smart city scenarios
"""


class C(BaseConstants):
    NAME_IN_URL = 'city_scenarios'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    # ---------- constants used by the player class
    # default choice for all contributions
    DEF_CHOICES = [[0,"none (cost=0)"], [1,"low (cost=1)"],[2,"high (cost=2)"]]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    # variables that will hold choice of contribution for every scenario
    bike_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    bus_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    crack_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    drain_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    graffiti_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    hydrant_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    bench_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    stopsign_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    streetlight_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)
    trash_contribution = models.CurrencyField(widget=RadioSelect, choices=C.DEF_CHOICES)


# -------------------- FUNCTIONS --------------------
def set_payoffs(group: Group):
    # players = group.get_players()
    # contributions = [p.contribution for p in players]
    # group.total_contribution = sum(contributions)
    # group.individual_share = (
    #     group.total_contribution / C.PLAYERS_PER_GROUP
    # )
    # for p in players:
    #     p.payoff = C.ENDOWMENT - p.contribution + group.individual_share
    pass

# -------------------- PAGES --------------------
class AllScenes(Page):
    form_model = 'player'
    form_fields = ["bike_contribution", "bus_contribution", "crack_contribution",
                   "drain_contribution", "graffiti_contribution", "hydrant_contribution",
                   "bench_contribution", "stopsign_contribution", "streetlight_contribution",
                   "trash_contribution"]


class BikeBusCrack(Page):
    form_model = 'player'
    form_fields = ["bike_contribution", "bus_contribution", "crack_contribution"]


class WaitForPlayers(WaitPage):
    title_text = "Waiting for players"
    body_text = "Please wait for all players"
    after_all_players_arrive = set_payoffs


class Feedback(Page):
    form_model = 'player'


page_sequence = [BikeBusCrack, WaitForPlayers, Feedback]

