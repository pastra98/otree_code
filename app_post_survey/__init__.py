################################################################################
##                   POST SURVEY APP                                          ##
################################################################################

from otree.api import *
from otree.forms.widgets import RadioSelect as rs

doc = """
get post game survey data
"""

class C(BaseConstants):
    NAME_IN_URL = "post_survey"
    NUM_ROUNDS = 1
    PLAYERS_PER_GROUP = None


class Player(BasePlayer):
    # just a test for now
    country = models.StringField(widget=rs, choices=["Austria", "Germany", "Switzerland"])


# -------------------- UNUSED CLASSES -------------------- 

class Group(BaseGroup):
    pass

class Subsession(BaseSubsession):
    pass

# -------------------- PAGES --------------------

class PostSurvey(Page):
    form_model = "player"
    form_fields = ["country"]

class CompletionConfirmation(Page):
    pass

page_sequence = [PostSurvey, CompletionConfirmation]