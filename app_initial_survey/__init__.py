################################################################################
##                   INCOME SURVEY APP                                        ##
################################################################################

from otree.api import *
import random
from datetime import datetime as dt


doc = """
get initial ses information
"""

class C(BaseConstants):
    NAME_IN_URL = "initial_survey"
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = None # also needs to be included
    FB_TREATMENTS = ["competitive", "cooperative", "control"]


class Player(BasePlayer):
    # just a test for now
    income = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    understood_game = models.BooleanField(label="Did you understand the game?", choices=[[True, 'Yes'], [False, 'No']])


# -------------------- UNUSED CLASSES -------------------- 

class Group(BaseGroup):
    # apparently need to include this definition
    pass

class Subsession(BaseSubsession):
    # normally creating_session should be used to assign treatments and part. labels
    # but it didn't work there, so it's done in the waitpage
    pass

# -------------------- PAGES --------------------

class Explanation(Page):
    form_model = "player"
    form_fields = ["understood_game"]


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
            print(f"{players} were assigned to {treatment}")

        players = group.get_players()
        # check number of playas divisible by 4 - allows for unequal treament sizes
        if len(players) % 4 != 0:
            raise Exception("Number of players must be divisible by 3")
        # if yes, assign treatments to participants
        else:
            random.shuffle(players)
            for i in range(0, len(players), 4):
                batch = players[i:i+4]
                treatment = C.FB_TREATMENTS[i // 4 % len(C.FB_TREATMENTS)]
                assign_treatments(batch, treatment)

        ##################################################
        # normally this is done in creating_session in subsession class, but it didn't work there
        for player in group.subsession.get_players():
            participant = player.participant
            time = dt.now().strftime('%Y-%m-%d_%H:%M')
            sesh_code = group.subsession.session.code
            participant.label = f"P{participant.id_in_session}-{sesh_code}-{time}"
        ##################################################


# page_sequence = [Explanation, IncomeSurvey, WaitForPlayers]
page_sequence = [IncomeSurvey, WaitForPlayers]