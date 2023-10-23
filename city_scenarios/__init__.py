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
    # ---------- all existing pages # TODO: this could be more beautiful
    PAGES = [SCENARIOS[0:3], SCENARIOS[3:6], SCENARIOS[6:9]]
    NUM_ROUNDS = len(PAGES)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    # generate class attributes for all scenarios with _contribution suffix
    # for scenario in C.SCENARIOS:
    #     locals()[f"{scenario}_contribution"] = models.CurrencyField(min=0, max=C.ENDOWMENT)
    bike_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    bus_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    crack_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    drain_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    graffiti_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    hydrant_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    bench_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    stopsign_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    streetlight_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    trash_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)

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
        return [s+"_contribution" for s in C.PAGES[player.round_number-1]]

    @staticmethod
    def vars_for_template(player):
        return {"img1": f"city_pics/{C.PAGES[player.round_number-1][0]}.jpg",
                "img2": f"city_pics/{C.PAGES[player.round_number-1][1]}.jpg",
                "img3": f"city_pics/{C.PAGES[player.round_number-1][2]}.jpg",
                "name1": C.PAGES[player.round_number-1][0],
                "name2": C.PAGES[player.round_number-1][1],
                "name3": C.PAGES[player.round_number-1][2]}


class WaitForPlayers(WaitPage):
    title_text = "Waiting for players"
    body_text = "Please wait for all players"
    # after_all_players_arrive = set_payoffs


class Feedback(Page):
    form_model = 'player'


page_sequence = [Scenario, WaitForPlayers, Feedback] # should repeat for NUM_ROUNDS