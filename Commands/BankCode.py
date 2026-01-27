from Core.Response import Response


def execute(config):
    """
    get ip address of our
    :param config:
    :return:
    """
    try:
        ip_address = config.get("host")
        return Response.success("BC", ip_address)
    except Exception as e:
        return Response.error(f"ER Error getting bank code: {str(e)}")
