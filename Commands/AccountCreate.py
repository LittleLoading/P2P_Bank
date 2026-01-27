from Core.Response import Response


def execute(config, db):
    try:
        my_ip = config.get("host")

        acc_num = db.get_next_free_account_number()

        if acc_num is None:
            return Response.error("ER Bank is full (limit 99999 reached).")

        if db.add_account(acc_num):
            return Response.success("AC", f"{acc_num}/{my_ip}")
        else:
            return Response.error("ER Couldn't create database account.")

    except Exception as e:
        return Response.error(f"ER Critical error while AC: {str(e)}")
