from otree.api import *
# from otree.forms.widgets import RadioSelect

# TODO:


doc = """
Testing the smart city scenarios
"""



class C(BaseConstants):
    NAME_IN_URL = 'city_scenarios'
    PLAYERS_PER_GROUP = 2
    ENDOWMENT = cu(10)
    # ---------- Constats used by the player class
    # default choice for all contributions
    DEF_CHOICES = [[0,"none (cost=0)"], [1,"low (cost=1)"],[2,"high (cost=2)"]]
    # multiplier for the individual share
    MULTIPLIER = 2
    # ---------- all existing scenarios
    SCENARIOS = ["bike", "bus", "crack", "drain", "graffiti", "hydrant", "bench",
        "stopsign", "streetlight", "trash"]
    NUM_ROUNDS = len(SCENARIOS)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
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
        return [f"{C.SCENARIOS[player.round_number-1]}_contribution"]

    @staticmethod
    def vars_for_template(player):
        scenario = C.SCENARIOS[player.round_number-1]
        return {"img": f"city_pics/{scenario}.jpg",
                "name": scenario}


class WaitForPlayers(WaitPage):
    title_text = "Waiting for players"
    body_text = "Please wait for all players"
    # after_all_players_arrive = "set_payoffs"

    def after_all_players_arrive(group):
        players = group.get_players()
        scenario = C.SCENARIOS[group.round_number-1]
        contributions = [getattr(p, f"{scenario}_contribution") for p in players]
        group.total_contribution = sum(contributions)
        group.individual_share = group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
        for player in players:
            player.payoff = C.ENDOWMENT - getattr(player, f"{scenario}_contribution") + group.individual_share


class Feedback(Page):
    form_model = 'player'

    # broken please fix
    @staticmethod
    def vars_for_template(player):
        group = player.group
        scenario = C.SCENARIOS[group.round_number-1]
        contributions = getattr(player, f"{scenario}_contribution")
        total_group_contribution = group.total_contribution
        if total_group_contribution > 0:
            contribution_percentage = (contributions / total_group_contribution) * 100
        else:
            contribution_percentage = 0
        return {
            'contribution_percentage': 0,
        }


page_sequence = [Scenario, WaitForPlayers, Feedback] # should repeat for NUM_ROUNDS