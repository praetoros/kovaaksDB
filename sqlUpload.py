import csvRestructure


def export_to_database(list_of_stats, db_token):
    for instance in list_of_stats:
        other_data_dict = csvRestructure.otherdata_to_dict(instance[1])

        insert_id = insert_data(other_data_dict, db_token)

        print(f'inserted ID: {insert_id} | {other_data_dict["data_fileName"]}')

        kill_data_dict = csvRestructure.killdata_to_dict(instance[2], insert_id)
        weapon_data_dict = csvRestructure.weapondata_to_dict(instance[3], insert_id)

        insert_kill(kill_data_dict, db_token)
        insert_weapon(weapon_data_dict, db_token)


def check_file_uploaded_bulk(file_names, db_token):  # TODO: add
    check_if_uploaded = db_token.cursor()
    placeholders = ', '.join('%s' for unused in file_names)
    check_if_uploaded_sql = "SELECT `data_fileName` FROM `tbl_data` where " \
                            "`data_deleted` = 0 AND " \
                            "`data_fileName` in (%s" % placeholders + ")"
    check_if_uploaded.execute(check_if_uploaded_sql, file_names)
    output = []
    for file in check_if_uploaded.fetchall():
        output.append(file[0])
    return output


def insert_data(other_data_dict, db_token):
    print(other_data_dict)
    new_upload = db_token.cursor()
    new_upload_sql = "INSERT INTO `tbl_data` " \
                     "(data_user, " \
                     "data_scenario, " \
                     "data_score, " \
                     "data_version, " \
                     "data_sensitivityH, " \
                     "data_sensitivityV, " \
                     "data_dpi, " \
                     "data_sensitivityType, " \
                     "data_resolution, " \
                     "data_fpsMax, " \
                     "data_fpsAvg, " \
                     "data_hash," \
                     "data_fileName) " \
                     "VALUES " \
                     "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    new_upload_val = (1,
                      other_data_dict.get("data_scenario", "none"),
                      other_data_dict.get("data_score", 0),
                      other_data_dict.get("data_version", 0),
                      other_data_dict.get("data_sensitivityH", 0),
                      other_data_dict.get("data_sensitivityV", 0),
                      other_data_dict.get("data_dpi", 0),
                      other_data_dict.get("data_sensitivityType", "none"),
                      other_data_dict.get("data_resolution", 0),
                      other_data_dict.get("data_fpsMax", 0),
                      other_data_dict.get("data_fpsAvg", 0),
                      other_data_dict.get("data_hash", "none"),
                      other_data_dict.get("data_fileName", "none"))
    new_upload.execute(new_upload_sql, new_upload_val)
    db_token.commit()
    return new_upload.lastrowid


def insert_kill(data, db_token):
    new_upload = db_token.cursor()
    new_upload_sql = "INSERT INTO `tbl_kill` " \
                     "(kill_user, " \
                     "kill_data, " \
                     "kill_number, " \
                     "kill_timestamp, " \
                     "kill_bot, " \
                     "kill_weapon, " \
                     "kill_ttk, " \
                     "kill_shots, " \
                     "kill_hits, " \
                     "kill_accuracy, " \
                     "kill_damageDone, " \
                     "kill_damagePossible," \
                     "kill_efficiency," \
                     "kill_cheated) " \
                     "VALUES " \
                     "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    new_upload.executemany(new_upload_sql, data)
    db_token.commit()
    return new_upload.lastrowid


def insert_weapon(data, db_token):
    new_upload = db_token.cursor()
    new_upload_sql = "INSERT INTO `tbl_weapon` " \
                     "(weapon_user, " \
                     "weapon_data, " \
                     "weapon_number, " \
                     "weapon_accuracy, " \
                     "weapon_weapon, " \
                     "weapon_shots, " \
                     "weapon_hits, " \
                     "weapon_damageDone, " \
                     "weapon_damagePotential) " \
                     "VALUES " \
                     "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    new_upload.executemany(new_upload_sql, data)
    db_token.commit()
    return new_upload.lastrowid
