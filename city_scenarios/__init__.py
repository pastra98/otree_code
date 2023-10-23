from otree.api import *
# from otree.forms.widgets import RadioSelect

# TODO:


doc = """
Testing the smart city scenarios
"""



class C(BaseConstants):
    NAME_IN_URL = 'city_scenarios'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    # ---------- Constats used by the player class
    # default choice for all contributions
    DEF_CHOICES = [[0,"none (cost=0)"], [1,"low (cost=1)"],[2,"high (cost=2)"]]
    # ---------- all existing scenarios
    SCENARIOS = ["bike", "bus", "crack", "drain", "graffiti", "hydrant", "bench",
        "stopsign", "streetlight", "trash"]
    # ---------- all existing pages # TODO: this could be more beautiful


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total = models.CurrencyField()
    individual_share = models.CurrencyField()


class Player(BasePlayer):
    # generate class attributes for all scenarios with _contribution suffix
    # for scenario in C.SCENARIOS:
    #     locals()[f"{scenario}_contribution"] = models.CurrencyField(min=0, max=C.ENDOWMENT)
    bike_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    bus_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    crack_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    drain_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    graffiti_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    hydrant_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    bench_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    stopsign_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    streetlight_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    trash_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)

# -------------------- FUNCTIONS --------------------
def check_effort(player: Player, timeout_happened):
    # check if player has spent too much of their endowment
    print(player.bike_contribution)


# -------------------- PAGES --------------------
class AllScenes(Page):
    form_model = 'player'
    form_fields = C.SCENARIOS


class ScenarioPage(Page):
    form_model = 'player'
    scenario_names = [] # this might also be dumb

    # call to check if player has spent too much of their endowment here
    before_next_page = check_effort

class Scenario1(ScenarioPage):
    # must be a class definition, cannot use instances for scenarios
    # otree is seriously weird. would be cool to validate scenarios here
    scenario_names = ["bike", "bus", "crack"]
    form_fields = [f"{scenario}_contribution" for scenario in scenario_names]

    template_dict = {}
    for i, name in enumerate(scenario_names):
        template_dict[f"name{i+1}"] = name
        template_dict[f"img{i+1}"] = f"city_pics/{name}.jpg"
    # solution - define whatever the page needs in the constants
    @classmethod
    def vars_for_template(player):
        return C.template_dict


class WaitForPlayers(WaitPage):
    title_text = "Waiting for players"
    body_text = "Please wait for all players"
    # after_all_players_arrive = set_payoffs


class Feedback(Page):
    form_model = 'player'


page_sequence = [Scenario1, WaitForPlayers, Feedback]