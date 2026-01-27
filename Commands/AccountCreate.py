from Core.Response import Response


def execute(config, db):
    """
    create and insert new bank account to db
    :param config: {'host': '127.0.0.1', 'port': 65525, 'timeout': 20} for myip address
    :param db: database connection
    :return: success or error response
    """
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
