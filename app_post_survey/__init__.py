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
        "Early childhood education (e.g. play school, Kindergarten)", 
        "Primary education (elementary school)", 
        "Lower secondary education (e.g. middle school, AHS)",
        "Upper secondary education (e.g. High School, Gymnasium, Higher technical and vocational college)",
        "Post-secondary non-tertiary education (e.g. Career, technical or professional training programmes, Professional Certificates)",
        "Bachelor's degree or equivalent level", 
        "Master's degree or equivalent level", 
        "Doctoral degree or equivalent level"
    ]



class Player(BasePlayer):
    country = models.StringField(
        choices=["Austria", "Germany", "Switzerland", "France", "Italy", "Other"],
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
        choices=[
            "Legislators, senior officials and managers",
            "Professionals",
            "Technicians and associate professionals",
            "Clerks",
            "Service workers and shop and market sales workers",
            "Skilled agricultural, forestry and fishery workers",
            "Craft and related trade workers",
            "Plant and machine operators and assemblers",
            "Elementary occupations",
            "Armed forces occupation",
            "None of the above"
        ],
        label="What is your main occupation? If you’re studying, unemployed or are not covering your own expenses, please choose the main occupation of one of your parents (one where monthly earnings are most likely to be higher)",
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
            "Prefer not to answer"
        ],
        label="Who lives in your household (including you)?",
        widget=rs
    )

    number_of_books = models.StringField(
        choices=[
            "None or a few (0--10 books)",
            "Enough to fill half a shelf (11--25 books)",
            "Enough to fill two bookshelves (101–200 books)",
            "Enough to fill three or more bookshelves (more than 200 books)"
        ],
        label="How many books do you have at home?",
        widget=rs)
    income = models.StringField(
        choices=[
            "< 10.000€",
            "10.000€ - 19.999€",
            "20.000 - 29.999€",
            "30.000 - 34.999€",
            "35.000 - 49.999€",
            "50.000 - 64.999€",
            "> 65.000€"
        ],
        label="Please estimate the bracket into which your yearly net amount of your income falls from all sources, wages, public assistance/benefits, help from relatives, alimony, and so on.",
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
        'income',
    ]
    timeout_seconds = 120


class CompletionConfirmation(Page):
    pass

page_sequence = [PostSurvey, CompletionConfirmation]