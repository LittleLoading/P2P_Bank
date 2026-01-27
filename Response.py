class Response:
    @staticmethod
    def success(command, message=""):
        """
        Returns success message of some process.
        :param command: Command that was successful.
        :param message: Message of success, unique for each command.
        :return: string
        """
        messg = f"{command.upper()} {message}".strip()
        return f"{messg}\n"

    @staticmethod
    def error(message):
        """
        Return error messages.
        :param message: string error message
        :return: string
        """
        return f"ERROR: {message}\n"

