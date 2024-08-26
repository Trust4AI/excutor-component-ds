import os

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'generator_api', 'templates')
GENDER_AND_SEXUAL_ORIENTATION_PATH = 'gender_and_sexual_orientation'
RACE_AND_NATIONALITY_PATH = 'race_and_nationality'
YES_NO_PATH = 'yes_no'
THREE_REASONS_PATH = 'three_reasons'
MC_PATH = 'mc'

GENDER_AND_SEXUAL_ORIENTATION_YES_NO_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH,
                                                                  GENDER_AND_SEXUAL_ORIENTATION_PATH,
                                                                  YES_NO_PATH)
GENDER_AND_SEXUAL_ORIENTATION_THREE_REASONS_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH,
                                                                         GENDER_AND_SEXUAL_ORIENTATION_PATH,
                                                                         THREE_REASONS_PATH)
GENDER_AND_SEXUAL_ORIENTATION_MC_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH,
                                                              GENDER_AND_SEXUAL_ORIENTATION_PATH,
                                                              MC_PATH)

RACE_AND_NATIONALITY_YES_NO_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH,
                                                         RACE_AND_NATIONALITY_PATH,
                                                         YES_NO_PATH)

RACE_AND_NATIONALITY_THREE_REASONS_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH,
                                                                RACE_AND_NATIONALITY_PATH,
                                                                THREE_REASONS_PATH)

RACE_AND_NATIONALITY_MC_TEMPLATE_PATH = os.path.join(TEMPLATE_PATH,
                                                     RACE_AND_NATIONALITY_PATH,
                                                     MC_PATH)

PATHS = {
    #'gender_and_sexual_yes_no': GENDER_AND_SEXUAL_ORIENTATION_YES_NO_TEMPLATE_PATH,
    'gender_and_sexual_three_reasons': GENDER_AND_SEXUAL_ORIENTATION_THREE_REASONS_TEMPLATE_PATH,
    'gender_and_sexual_mc': GENDER_AND_SEXUAL_ORIENTATION_MC_TEMPLATE_PATH,
    'race_and_nationality_yes_no': RACE_AND_NATIONALITY_YES_NO_TEMPLATE_PATH,
    #'race_and_nationatily_three_reasons': RACE_AND_NATIONALITY_THREE_REASONS_TEMPLATE_PATH,
    #'race_adn_nationality_mc': RACE_AND_NATIONALITY_MC_TEMPLATE_PATH
}

RESULTS_EXPERIMENT_PATH = os.path.join(os.path.dirname(__file__), 'results_experiment')


def check_paths(name, path):
    if os.path.exists(path):
        print(f'{name} -- {path} --> exists')
    else:
        print(f'{name} -- {path} --> does not exist')


if __name__ == '__main__':
    for k, v in PATHS.items():
        check_paths(k, v)
