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
    # for the survey
    EDUCATION_LEVEL_CHOICES = [
        "No schooling", 
        "Early childhood education", 
        "Primary education", 
        "Lower secondary education",
        "Upper secondary education", 
        "Post-secondary non-tertiary education",
        "Bachelor's or equivalent level", 
        "Master's or equivalent level", 
        "Doctoral or equivalent level"
    ]



class Player(BasePlayer):
    country = models.StringField(
        choices=["Austria", "Germany", "Switzerland", "France", "Italy"],
        label="In which country do you currently live?",
        widget=rs)

    education_level = models.StringField(
        choices=C.EDUCATION_LEVEL_CHOICES,
        label="What is your highest level of education?",
        widget=rs)

    mothers_education_level = models.StringField(
        choices=C.EDUCATION_LEVEL_CHOICES,
        label="What is the highest level of education of your mother?",
        widget=rs)

    fathers_education_level = models.StringField(
        choices=C.EDUCATION_LEVEL_CHOICES,
        label="What is the highest level of education of your father?",
        widget=rs)

    occupation = models.StringField(
        choices=["Managers", "Professionals", "Technicians and associate professionals", ...],
        label="What is your main occupation?",
        widget=rs)

    household_composition = models.StringField(
        choices=[
            "One person (just me)",
            "One person and one child",
            "One person and two children",
            "Two persons",
            "Two persons and one child",
            "Two persons and two children",
            "Two persons and three children",
            "Three persons",
            "Three persons and one child",
            "Four persons",
            "Other",
            "No answer"
        ],
        label="Who lives in your household (including you)?",
        widget=rs
    )

    number_of_books = models.StringField(
        choices=["None or a few (0--10 books)", "Enough to fill half a shelf (11--25 books)", ...],
        label="How many books do you have at home?",
        widget=rs)

    # Cultural activities frequency
    cultural_activities_frequency = models.StringField(
        choices=["Not at all", "Once or twice", "Three or four times", "More than four times"],
        label="In the past 12 months, how often did you do the following activities? (Theater, lectures, museums, etc.)",
        widget=rs)



# -------------------- UNUSED CLASSES -------------------- 

class Group(BaseGroup):
    pass

class Subsession(BaseSubsession):
    pass

# -------------------- PAGES --------------------

class PostSurvey(Page):
    form_model = "player"
    form_fields = [
        'country',
        'education_level',
        'mothers_education_level',
        'fathers_education_level',
        'occupation',
        'household_composition',
        'number_of_books',
        'cultural_activities_frequency'
    ]


class CompletionConfirmation(Page):
    pass

page_sequence = [PostSurvey, CompletionConfirmation]