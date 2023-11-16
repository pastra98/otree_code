from otree.api import *
# from otree.forms.widgets import RadioSelect

# TODO:


doc = """
Testing the smart city scenarios
"""



class C(BaseConstants):
    NAME_IN_URL = 'city_scenarios'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    # ---------- Constats used by the player class
    # default choice for all contributions
    DEF_CHOICES = [[0,"none (cost=0)"], [1,"low (cost=1)"],[2,"high (cost=2)"]]
    # ---------- all existing scenarios
    SCENARIOS = ["bike", "bus", "crack", "drain", "graffiti", "hydrant", "bench",
        "stopsign", "streetlight", "trash"]
    NUM_ROUNDS = len(SCENARIOS)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    # generate class attributes for all scenarios with _contribution suffix
    for scenario in C.SCENARIOS:
        locals()[f"{scenario}_contribution"] = models.CurrencyField(min=0, max=C.ENDOWMENT)
# -------------------- FUNCTIONS --------------------

# -------------------- PAGES --------------------

class Scenario(Page):
    form_model = 'player'
    form_fields = [s+"_contribution" for s in C.SCENARIOS] # all scenarios

    @staticmethod
    def error_message(player, values):
        total_spend = sum(values.values()) # this works because there are no other forms here
        if total_spend > C.ENDOWMENT:
            return f"You have spent {total_spend} but only have {C.ENDOWMENT} to spend"

    @staticmethod
    def get_form_fields(player):
        return [f"{C.SCENARIOS[player.round_number-1]}_contribution"]

    @staticmethod
    def vars_for_template(player):
        scenario = C.SCENARIOS[player.round_number-1]
        return {"img": f"city_pics/{scenario}.jpg",
                "name": scenario}


class WaitForPlayers(WaitPage):
    title_text = "Waiting for players"
    body_text = "Please wait for all players"
    # after_all_players_arrive = set_payoffs


class Feedback(Page):
    form_model = 'player'


page_sequence = [Scenario, WaitForPlayers, Feedback] # should repeat for NUM_ROUNDS