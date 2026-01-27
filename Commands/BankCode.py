from Core.Response import Response


def execute(config):
    """

    """
    try:
        ip_address = config.get("host", "127.0.0.1")
        return Response.success("BC", ip_address)
    except Exception as e:
        return Response.error(f"ER Chyba pri ziskavani kodu banky: {str(e)}")
