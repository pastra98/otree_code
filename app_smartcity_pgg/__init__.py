################################################################################
##                   PUBLIC GOODS GAME APP                                    ##
################################################################################

from otree.api import *
from otree.forms.widgets import RadioSelect as rs

doc = """
Testing the smart city scenarios
"""

class C(BaseConstants):
    NAME_IN_URL = "city_scenarios"
    PLAYERS_PER_GROUP = 4 # change this to 4 later

    # ---------- Constants for endowment function
    MULTIPLIER = 1.5 # multiplier for the individual share
    HIGH_ENDOW = 6
    LOW_ENDOW = 4

    # ---------- all existing scenarios
    # SCENARIOS = ["bike", "bus", "crack", "drain", "graffiti", "hydrant", "bench"]
    NUM_ROUNDS = 7
    SCENARIOS = [f"s{i+1}" for i in range(NUM_ROUNDS)] # s1 to s7


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_spend = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    # this is fucking stupid, but it needs to be a field
    endowment = models.CurrencyField(initial=0)

    # todo maybe the field max value can be dynamically assigned based on endowment
    s1_contribution = models.CurrencyField(widget=rs, choices=[0,1,2,3,4])
    s2_contribution = models.CurrencyField(widget=rs, choices=[0,1,2,3,4])
    s3_contribution = models.CurrencyField(widget=rs, choices=[0,1,2,3,4])
    s4_contribution = models.CurrencyField(widget=rs, choices=[0,1,2,3,4])
    s5_contribution = models.CurrencyField(widget=rs, choices=[0,1,2,3,4])
    s6_contribution = models.CurrencyField(widget=rs, choices=[0,1,2,3,4])
    s7_contribution = models.CurrencyField(widget=rs, choices=[0,1,2,3,4])

# -------------------- FUNCTIONS --------------------

# this function ensures that only players with the same feedback treatment are grouped together
def group_by_arrival_time_method(subsession, waiting_players):
    # Define the required number of players with each SES in a group
    REQUIRED_LOW_SES = REQUIRED_HIGH_SES = C.PLAYERS_PER_GROUP // 2

    # Group players by feedback treatment
    control = [p for p in waiting_players if p.participant.fb_treat == "control"]
    competitive = [p for p in waiting_players if p.participant.fb_treat == "competitive"]
    cooperative = [p for p in waiting_players if p.participant.fb_treat == "cooperative"]

    # Function to form groups with balanced SES
    def form_group(players):
        low_ses_players = [p for p in players if p.participant.ses_treat == "low"]
        high_ses_players = [p for p in players if p.participant.ses_treat == "high"]

        if len(low_ses_players) >= REQUIRED_LOW_SES and len(high_ses_players) >= REQUIRED_HIGH_SES:
            return low_ses_players[:REQUIRED_LOW_SES] + high_ses_players[:REQUIRED_HIGH_SES]
        else:
            return None

    # Try to form groups for each treatment
    for treatment_group in [control, competitive, cooperative]:
        group = form_group(treatment_group)
        if group:
            return group

    # If not enough players are available in any treatment, return None to keep waiting
    return None

# -------------------- PAGES --------------------

class Scenario(Page):
    form_model = 'player'
    form_fields = [s+"_contribution" for s in C.SCENARIOS] # all scenarios
    timeout_seconds = 90

    @staticmethod
    def error_message(player, values):
        contribution = sum(values.values()) # this works because there are no other forms here
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
        return {"img1": f"city_pics/{scenario}/{scenario}1.jpg",
                "img2": f"city_pics/{scenario}/{scenario}2.jpg",
                "img3": f"city_pics/{scenario}/{scenario}3.jpg",
                "img4": f"city_pics/{scenario}/{scenario}4.jpg",
                "img5": f"city_pics/{scenario}/{scenario}5.jpg",
                "name": scenario,
                "formname": f"{C.SCENARIOS[player.round_number-1]}_contribution",
                }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            current_scenario = C.SCENARIOS[player.round_number-1]
            if getattr(player, f"{current_scenario}_contribution") is None:
                setattr(player, f"{current_scenario}_contribution", 0)  # Default value

    

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
            player.participant.total_points += player.payoff


class Feedback(Page):
    form_model = 'player'
    timeout_seconds = 30

    @staticmethod
    def vars_for_template(player):
        group = player.group
        scenario = C.SCENARIOS[group.round_number-1]
        player_contrib = getattr(player, f"{scenario}_contribution")

        # determine if current player contributes more than 50% of the group members
        spent_more_than, spent_as_much_as  = 0, 0
        for p in group.get_players():
            if p != player:
                if player_contrib > getattr(p, f"{scenario}_contribution"):
                    spent_more_than += 1
                elif player_contrib == getattr(p, f"{scenario}_contribution"):
                    spent_as_much_as += 1
        outspent_percent = round((spent_more_than / (len(group.get_players())-1)) * 100, 2)

        # group spending relative percent
        if group.total_spend > 0:
            contribution_percentage = round((float(player_contrib) / float(group.total_spend)) * 100, 2)
        else:
            contribution_percentage = 0

        return {
            "contribution_percent": contribution_percentage,
            "feedback_treat": player.participant.fb_treat,
            "outspent_percent": outspent_percent,
            "spentmore_percent": outspent_percent ,
            "spent_more_than": spent_more_than,
            "spent_as_much_as": spent_as_much_as,
            "spent_less_than": C.PLAYERS_PER_GROUP - spent_more_than - spent_as_much_as - 1,
            "player_contrib": player_contrib,
            "group_total": group.total_spend,
            "participant_total": player.participant.total_points,
            "scenario": scenario
        }

class AssignGroupWait(WaitPage):
    title_text = "Waiting for players"
    body_text = "Waiting for players"
    group_by_arrival_time = True


page_sequence = [AssignGroupWait, Scenario, WaitForPlayers, Feedback] # should repeat for NUM_ROUNDS