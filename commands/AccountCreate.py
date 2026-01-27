from Core.Response import Response


def execute(config, db):
    try:
        my_ip = config.get("host")

        acc_num = db.get_next_free_account_number()

        if acc_num is None:
            return Response.error("ER Banka je plně obsazena (dosazeno limitu 99999).")

        if db.add_account(acc_num):
            return Response.success("AC", f"{acc_num}/{my_ip}")
        else:
            return Response.error("ER Nepodařilo se vytvořit účet v databázi.")

    except Exception as e:
        return Response.error(f"ER Kritická chyba při AC: {str(e)}")