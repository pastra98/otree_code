from otree.api import *

doc = """
Testing the smart city scenarios
"""

class C(BaseConstants):
    NAME_IN_URL = 'city_scenarios'
    PLAYERS_PER_GROUP = 2

    # ---------- Constants used by the player class
    # default choice for all contributions
    DEF_CHOICES = [[0,"none (cost=0)"], [1,"low (cost=1)"],[2,"high (cost=2)"]]

    # ---------- Constants for endowment function
    MULTIPLIER = 2 # multiplier for the individual share
    HIGH_ENDOW = 4
    LOW_ENDOW = 3

    # ---------- all existing scenarios
    SCENARIOS = ["bike", "bus", "crack", "drain", "graffiti", "hydrant", "bench",
        "stopsign", "streetlight", "trash"]
    NUM_ROUNDS = len(SCENARIOS)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_spend = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    # this is fucking stupid, but it needs to be a field
    endowment = models.CurrencyField(initial=0)

    # todo maybe the field max value can be dynamically assigned based on endowment
    bike_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    bus_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    crack_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    drain_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    graffiti_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    hydrant_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    bench_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    stopsign_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    streetlight_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)
    trash_contribution = models.CurrencyField(min=0, max=C.HIGH_ENDOW)

# -------------------- FUNCTIONS --------------------

# -------------------- PAGES --------------------

class Scenario(Page):
    form_model = 'player'
    form_fields = [s+"_contribution" for s in C.SCENARIOS] # all scenarios

    @staticmethod
    def error_message(player, values):
        print(player.endowment)

        contribution = sum(values.values()) # this works because there are no other forms here
        # if total_spend > C.ENDOWMENT:
        if contribution > player.endowment:
            return f"You have spent {contribution} but only have {player.endowment} to spend"

    @staticmethod
    def get_form_fields(player):
        # assign player endowment in each round, important for max value in field
        player.endowment = C.HIGH_ENDOW if player.participant.ses_treatment == "high" else C.LOW_ENDOW

        return [f"{C.SCENARIOS[player.round_number-1]}_contribution"]

    @staticmethod
    def vars_for_template(player):
        scenario = C.SCENARIOS[player.round_number-1]
        return {"img": f"city_pics/{scenario}.jpg",
                "name": scenario}
    

class WaitForPlayers(WaitPage):
    title_text = "Waiting for players"
    body_text = "Please wait for all players"

    def after_all_players_arrive(group):
        players = group.get_players()
        scenario = C.SCENARIOS[group.round_number-1]
        contributions = [getattr(p, f"{scenario}_contribution") for p in players]
        group.total_spend = sum(contributions)
        # todo, calculate group size dynamically here
        group.individual_share = group.total_spend * C.MULTIPLIER / C.PLAYERS_PER_GROUP

        for player in players:
            player.payoff = (
                player.endowment -
                getattr(player, f"{scenario}_contribution") +
                group.individual_share
                )


class Feedback(Page):
    form_model = 'player'

    @staticmethod
    def vars_for_template(player):
        group = player.group
        scenario = C.SCENARIOS[group.round_number-1]
        contributions = getattr(player, f"{scenario}_contribution")
        
        print(contributions)
        print(group.total_spend)
        # todo, refactor this shit
        if group.total_spend > 0:
            contribution_percentage = (contributions / group.total_spend) * 100
        else:
            contribution_percentage = 0
        return {
            'contribution_percentage': contribution_percentage,
        }


page_sequence = [Scenario, WaitForPlayers, Feedback] # should repeat for NUM_ROUNDS