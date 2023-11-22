################################################################################
##                   PUBLIC GOODS GAME APP                                    ##
################################################################################

from otree.api import *

doc = """
Testing the smart city scenarios
"""

class C(BaseConstants):
    NAME_IN_URL = "city_scenarios"
    PLAYERS_PER_GROUP = 2 # change this to 4 later

    # ---------- Constants for feedback page
    FEEDBACK_DICT = {
        "control": "I have nothing to say",
        "competitive": "You suck, lolz git gud",
        "cooperative": "Kumbaya, spread the love"
    }

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

# this function ensures that only players with the same feedback treatment are grouped together
def group_by_arrival_time_method(subsession, waiting_players):

    # Group players by feedback treatment
    control = [p for p in waiting_players if p.participant.fb_treat == "control"]
    competitive = [p for p in waiting_players if p.participant.fb_treat == "competitive"]
    cooperative = [p for p in waiting_players if p.participant.fb_treat == "cooperative"]

    # Assign players to groups when enough players are available for each treatment
    if len(control) >= C.PLAYERS_PER_GROUP:
        return control[:C.PLAYERS_PER_GROUP]
    elif len(competitive) >= C.PLAYERS_PER_GROUP:
        return competitive[:C.PLAYERS_PER_GROUP]
    elif len(cooperative) >= C.PLAYERS_PER_GROUP:
        return cooperative[:C.PLAYERS_PER_GROUP]

    # If not enough players are available in any treatment, return None to keep waiting
    return None

# -------------------- PAGES --------------------

class Scenario(Page):
    form_model = 'player'
    form_fields = [s+"_contribution" for s in C.SCENARIOS] # all scenarios

    @staticmethod
    def error_message(player, values):
        contribution = sum(values.values()) # this works because there are no other forms here
        # if total_spend > C.ENDOWMENT:
        if contribution > player.endowment:
            return f"You have spent {contribution} but only have {player.endowment} to spend"

    @staticmethod
    def get_form_fields(player):
        # assign player endowment in each round, important for max value in field
        player.endowment = C.HIGH_ENDOW if player.participant.ses_treat == "high" else C.LOW_ENDOW
        # return the form field for the current scenario
        return [f"{C.SCENARIOS[player.round_number-1]}_contribution"]

    @staticmethod
    def vars_for_template(player):
        scenario = C.SCENARIOS[player.round_number-1]
        return {"img": f"city_pics/{scenario}.jpg",
                "name": scenario,
                }
    

class WaitForPlayers(WaitPage):
    title_text = "Waiting for players"
    body_text = "Please wait for all players"

    def after_all_players_arrive(group):
        players = group.get_players()
        scenario = C.SCENARIOS[group.round_number-1]
        contributions = [getattr(p, f"{scenario}_contribution") for p in players]
        group.total_spend = sum(contributions)
        # todo, is it possible to set group size dynamically??
        group.individual_share = group.total_spend * C.MULTIPLIER / len(players)

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
        # get feedback message based on player treatment
        fb = C.FEEDBACK_DICT[player.participant.fb_treat]

        # todo, refactor this shit
        if group.total_spend > 0:
            contribution_percentage = round((float(contributions) / float(group.total_spend)) * 100, 2)
        else:
            contribution_percentage = 0
        return {
            'contribution_percentage': contribution_percentage,
            "feedback": fb
        }

class AssignGroupWait(WaitPage):
    title_text = "Waiting for players"
    body_text = "Waiting for players"
    group_by_arrival_time = True


page_sequence = [AssignGroupWait, Scenario, WaitForPlayers, Feedback] # should repeat for NUM_ROUNDS