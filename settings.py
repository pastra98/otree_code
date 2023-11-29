from os import environ

SESSION_CONFIGS = [
    dict(
        name="real_session",
        display_name="Smart City Survey - Real Session",
        app_sequence=["app_initial_survey", "app_smartcity_pgg", "app_post_survey"],
        num_demo_participants=12,  # Set a reasonable number for testing
        use_browser_bots=False,    # Disable browser bots for real sessions
    )
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, 
    participation_fee=0.00, 
    doc="",
    experiment_started=False,  # Add this to control the manual start of the session
)

PARTICIPANT_FIELDS = ["ses_treat", "fb_treat"]
SESSION_FIELDS = ["experiment_started"]

LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ADMIN_USERNAME = 'admin'

# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Welcome to the smartcity experiment.
"""

SECRET_KEY = '3088493198341'

INSTALLED_APPS = ['otree']

ROOMS = [
    dict(
        name='smart_city_room',
        display_name='Smart City Experiment Room',
        # use_secure_urls=False,
    )
]
