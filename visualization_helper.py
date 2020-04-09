import numpy as np
import pycountry


def data_preprocess(data):
    """
    :param data:
    :return: clean data
    """
    data = data.replace(np.NaN, 0)
    data["Wage (million, €)"] = data["Wage"].str.replace("€", "", case=False)
    data["Wage (million, €)"] = data["Wage (million, €)"].str.replace("K", "", case=False).astype(float)
    data["Wage (million, €)"] = data["Wage (million, €)"] / 1000

    data["Release Clause (million, €)"] = data["Release Clause"].str.replace("€", "", case=False).str.replace("M", "",
                                                                                                              case=False).astype(
        float).astype(float)

    data["Value (million, €)"] = data["Value"].str.replace("€", "", case=False).str.replace("M", "", case=False).astype(float).astype(float)

    data["Weight (lbs)"] = data["Weight"].str.replace("lbs", "", case=False).astype(float)

    for i, row in data.iterrows():
        height_list = row.Height.split("'")
        cm = (float(height_list[0]) * 12 + float(height_list[1])) * 2.54
        data.at[i, "Height (cm)"] = cm

    data["Flag"] = data["Flag"].str.replace(".org/", ".com/", case=False)
    data["Photo"] = data["Photo"].str.replace(".org/", ".com/", case=False)
    data["Photo"] = data["Photo"].str.replace("/4/19/", "/10/20/", case=False)
    data.Nationality.replace("England", "United Kingdom", inplace=True)
    data.Nationality.replace("Wales", "United Kingdom", inplace=True)
    data.Nationality.replace("Scotland", "United Kingdom", inplace=True)
    data.Nationality.replace("Northern Ireland", "Ireland", inplace=True)
    data.Nationality.replace("Republic of Ireland", "Ireland", inplace=True)
    data.Nationality.replace("Korea Republic", "Korea, Democratic People's Republic of", inplace=True)
    data.Nationality.replace("China PR", "China", inplace=True)
    data.Nationality.replace("Russia", "Russian Federation", inplace=True)
    data.Nationality.replace("Ivory Coast", "Côte d'Ivoire", inplace=True)
    data.Nationality.replace("Czech Republic", "Czechia", inplace=True)
    data.Nationality.replace("DR Congo", "Congo, The Democratic Republic of the", inplace=True)
    data.Nationality.replace("Bosnia Herzegovina", "Bosnia and Herzegovina", inplace=True)

    data["Nationality_ISO_alpha"] = data.Nationality
    for i, row in data.iterrows():
        if pycountry.countries.get(name=row.Nationality_ISO_alpha) is not None:
            data.at[i, 'Nationality_ISO_alpha'] = pycountry.countries.get(name=row.Nationality_ISO_alpha).alpha_3
            continue
        if pycountry.countries.get(common_name=row.Nationality_ISO_alpha) is not None:
            data.at[i, 'Nationality_ISO_alpha'] = pycountry.countries.get(common_name=row.Nationality_ISO_alpha).alpha_3
            continue
        if pycountry.countries.get(official_name=row.Nationality_ISO_alpha) is not None:
            data.at[i, 'Nationality_ISO_alpha'] = pycountry.countries.get(
                official_name=row.Nationality_ISO_alpha).alpha_3
            continue
    data.Nationality.replace("Korea, Democratic People's Republic of", "Korea Republic", inplace=True)
    data.Nationality.replace("Congo, The Democratic Republic of the", "DR Congo", inplace=True)
    return data


def get_dropdown_features():
    features = ["Age", "Wage (million, €)", "International Reputation", "Value (million, €)", "Potential", "Overall", "Height (cm)",
                "Weight (lbs)", "Release Clause (million, €)", "Strength", "Stamina"]
    opts = [{'label': i, 'value': i} for i in features]

    return features, opts


def get_country_list(data):
    return list(data.Nationality.unique())


def get_marker_list():
    return list(range(0, 1001, 50))


def get_player_attributes():
    return ['Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling',
            'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
            'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower',
            'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression',
            'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
            'Marking', 'StandingTackle', 'SlidingTackle']


def get_player_skills(clean_data):
    """
    To convert "88+2" => 90
    :return:
    """
    skills_list = ['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
                   'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
                   'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']
    for i, row in clean_data.iterrows():
        for column in skills_list:
            clean_data.at[i, column] = eval(str(row[column]))
    for column in skills_list:
        clean_data[column] = clean_data[column].astype(float)

    return skills_list, clean_data


def get_goalkeeper_attributes():
    return ['GKDiving', 'GKHandling',
            'GKKicking', 'GKPositioning', 'GKReflexes']
