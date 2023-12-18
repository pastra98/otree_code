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
    CORRECT_A = [None, 2, 3, 1]


class Player(BasePlayer):
    income = models.IntegerField(
        widget=widgets.RadioSelect,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    curr_question = models.IntegerField(initial=1)
    # Comprehension Questions
    q1 = models.StringField(
        label="How is your payout calculated in the experiment?",
        choices=[
            (1, "Your endowment - Your submitted effort points"),
            (2, "Your endowment - Your submitted effort points + Average points submitted by everyone * factor"),
            (3, "Your endowment + Average points submitted by everyone * factor"),
            (4, "Average points submitted by everyone")
        ],
        widget=widgets.RadioSelect
    )
    q2 = models.StringField(
        label="If you submitted all 4 effort points from your endowment of 4 points, and the other participants submitted 12 points, making a total of 16 points in the pot, what is your payout in this round?",
        choices=[
            (1, "4"),
            (2, "0"),
            (3, "6"),
            (4, "12")
        ],
        widget=widgets.RadioSelect
    )

# -------------------- UNUSED CLASSES -------------------- 

class Group(BaseGroup):
    # apparently need to include this definition
    pass

class Subsession(BaseSubsession):
    # normally creating_session should be used to assign treatments and part. labels
    # but it didn't work there, so it's done in the waitpage
    pass

# -------------------- FUNCTIONS --------------------
@staticmethod
def check_answer(player, values):
    selected_answer = int(values[f"q{player.curr_question}"])
    correct_answer = C.CORRECT_A[player.curr_question]
    if selected_answer == correct_answer:
        player.curr_question += 1
    else:
        return "Wrong answer, please try again"

# -------------------- PAGES --------------------

class Intro(Page):
    form_model = "player"
    timeout_seconds = 90


class QuestionPage(Page):
    form_model = "player"
    error_message = check_answer
    timeout_seconds = 90

# the questions
class Q1(QuestionPage):
    form_fields = ["q1"]

class Q2(QuestionPage):
    form_fields = ["q2"]


class IncomeSurvey(Page):
    form_model = "player"
    form_fields = ["income"]
    timeout_seconds = 90

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.income = 0



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
            raise Exception("Number of players must be divisible by 4")
        # if yes, assign treatments to participants
        else:
            random.shuffle(players)
            for i in range(0, len(players), 4):
                batch = players[i:i+4]
                treatment = C.FB_TREATMENTS[i // 4 % len(C.FB_TREATMENTS)]
                assign_treatments(batch, treatment)

        # normally this is done in creating_session in subsession class, but it didn't work there
        for player in group.subsession.get_players():
            participant = player.participant
            time = dt.now().strftime('%Y-%m-%d_%H:%M')
            sesh_code = group.subsession.session.code
            participant.label = f"P{participant.id_in_session}-{sesh_code}-{time}"
            # lastly, set total points to 0
            participant.total_points = 0


page_sequence = [Intro, Q1, Q2, IncomeSurvey, WaitForPlayers]