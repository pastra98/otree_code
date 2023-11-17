from otree.api import *
# from otree.forms.widgets import RadioSelect

# TODO:


doc = """
get initial ses information
"""



class C(BaseConstants):
    NAME_IN_URL = 'initial_survey'
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

    def after_all_players_arrive(group):
        # here we could:
        # 1. assign players to feedback treatments
        players = group.get_players()
        # 2. assign players to income treatments
        players.sort(key=lambda p: p.income)
        split_index = len(players) // 2 # todo figure out how to deal with guy in the middle/equal values
        [setattr(p.participant, 'ses_treatment', 'low') for p in players[:split_index]]
        [setattr(p.participant, 'ses_treatment', 'high') for p in players[split_index:]]

page_sequence = [IncomeSurvey, WaitForPlayers]