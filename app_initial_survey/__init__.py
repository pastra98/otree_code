################################################################################
##                   INCOME SURVEY APP                                        ##
################################################################################

from otree.api import *
import random

doc = """
get initial ses information
"""

class C(BaseConstants):
    NAME_IN_URL = "initial_survey"
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = None # also needs to be included


class Player(BasePlayer):
    # just a test for now
    income = models.CurrencyField(min=0)


# -------------------- UNUSED CLASSES -------------------- 

class Group(BaseGroup):
    # apparently need to include this definition
    pass

class Subsession(BaseSubsession):
    pass

# -------------------- PAGES --------------------

class IncomeSurvey(Page):
    form_model = "player"
    form_fields = ["income"]


class WaitForPlayers(WaitPage):
    title_text = "Waiting for players"
    body_text = "Please wait for all players"

    # called when all players completed income survey
    def after_all_players_arrive(group):
        # assign treatments is called for all treatment groups
        def assign_treatments(players, treatment):
            # 1. assign players to feedback treatments
            [setattr(p.participant, "fb_treat", treatment) for p in players]
            # 2. assign players to income treatments
            players.sort(key=lambda p: p.income)
            split_index = len(players) // 2 # todo figure out how to deal with guy in the middle/equal values
            [setattr(p.participant, "ses_treat", "low") for p in players[:split_index]]
            [setattr(p.participant, "ses_treat", "high") for p in players[split_index:]]

        players = group.get_players()
        # check number of playas divisible by 3
        if len(players) % 3 != 0:
            raise Exception("Number of players must be divisible by 3")
        # if yes, assign treatments to participants
        else:
            random.shuffle(players)
            third = len(players) // 3
            assign_treatments(players[:third], "control")
            assign_treatments(players[third:2*third], "competitive")
            assign_treatments(players[2*third:], "cooperative")
        

page_sequence = [IncomeSurvey, WaitForPlayers]