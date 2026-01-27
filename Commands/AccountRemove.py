from Response import Response


def execute(raw_parts, config, db):
    """
    Command: AR <account>/<ip>
    Logic: Removes the account only if balance is 0
    """
    try:
        if len(raw_parts) < 2:
            return Response.error("ER format of command is not correct")

        target_part = raw_parts[1]  # "10001/10.1.2.3"

        if "/" not in target_part:
            return Response.error("ER format of command is not correct")

        acc_num_str, bank_ip = target_part.split("/")

        if not acc_num_str.isdigit():
            return Response.error("ER format account number is not correct")

        acc_num = int(acc_num_str)
        my_ip = config.get("host")


        if bank_ip == my_ip:
            success, error_msg = db.delete_account(acc_num)
            if success:

                return Response.success("AR")
            else:
                return Response.error(error_msg)
        else:
            #PROXY LOGIC HERE!!!
            return Response.error(f"ER Bank {bank_ip} is not managed by this node.")

    except Exception as e:
        return Response.error(f"ER Error processing removal: {str(e)}")