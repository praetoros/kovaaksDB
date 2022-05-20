def otherdata_to_dict(data):
    other_data_dict = {}
    for data_type in data:
        match data_type[0]:
            case 'Scenario:':
                other_data_dict["data_scenario"] = data_type[1]
            case 'Score:':
                other_data_dict["data_score"] = data_type[1]
            case 'Game Version:':
                other_data_dict["data_version"] = data_type[1]
            case 'Horiz Sens:':
                other_data_dict["data_sensitivityH"] = data_type[1]
            case 'Vert Sens:':
                other_data_dict["data_sensitivityV"] = data_type[1]
            case 'DPI:':
                other_data_dict["data_dpi"] = data_type[1]
            case 'Sens Scale:':
                other_data_dict["data_sensitivityType"] = data_type[1]
            case 'Resolution:':
                other_data_dict["data_resolution"] = data_type[1]
            case 'Max FPS (config):':
                other_data_dict["data_fpsMax"] = data_type[1]
            case 'Avg FPS:':
                other_data_dict["data_fpsAvg"] = data_type[1]
            case 'Hash:':
                other_data_dict["data_hash"] = data_type[1]
            case 'fileName':
                other_data_dict["data_fileName"] = data_type[1]
    return other_data_dict


def killdata_to_dict(data):
    kill_data_dict = {}
    return kill_data_dict


def weapondata_to_dict(data):
    weapon_data_dict = {}
    return weapon_data_dict
