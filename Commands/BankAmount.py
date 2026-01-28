from Core.Response import Response


def execute(db):
    """
    Command: BA
    Format: BA <number>
    :param db: database connection
    :return: the total sum of all funds in the bank.
    """
    try:
        total_amount = db.get_total_bank_amount()
        return Response.success("BA", str(total_amount))
    except Exception as e:
        return Response.error(f"ER Error calculating bank amount: {str(e)}")
