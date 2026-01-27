from Core.Response import Response

def execute(db):
    """
    Command: BN
    Format: BN <number>
    :param db: database connection
    :return: Returns the number of clients currently having an account
    """
    try:
        client_count = db.get_total_clients_count()
        return Response.success("BN", str(client_count))
    except Exception as e:
        return Response.error(f"ER Error counting bank clients: {str(e)}")