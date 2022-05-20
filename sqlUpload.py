import csvRestructure


def export_to_database(list_of_stats, db_token):
    for instance in list_of_stats:
        other_data_dict = csvRestructure.otherdata_to_dict(instance[0])
        kill_data_dict = csvRestructure.killdata_to_dict(instance[1])
        weapon_data_dict = csvRestructure.weapondata_to_dict(instance[2])

        check_if_uploaded = db_token.cursor()
        check_if_uploaded_sql = "SELECT count(`data_fileName`) FROM `tbl_data` where `data_fileName` = %s"
        check_if_uploaded.execute(check_if_uploaded_sql, [other_data_dict["data_fileName"]])
        if check_if_uploaded.fetchone()[0] == 0:
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
                              other_data_dict["data_scenario"],
                              other_data_dict["data_score"],
                              other_data_dict["data_version"],
                              other_data_dict["data_sensitivityH"],
                              other_data_dict["data_sensitivityV"],
                              other_data_dict["data_dpi"],
                              other_data_dict["data_sensitivityType"],
                              other_data_dict["data_resolution"],
                              other_data_dict["data_fpsMax"],
                              other_data_dict["data_fpsAvg"],
                              other_data_dict["data_hash"],
                              other_data_dict["data_fileName"])
            new_upload.execute(new_upload_sql, new_upload_val)
            db_token.commit()

            print(f'inserted ID: {new_upload.lastrowid} | {other_data_dict["data_fileName"]}')
        else:
            print(f'already uploaded | {other_data_dict["data_fileName"]}')