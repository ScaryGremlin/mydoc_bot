from json import loads


def get_districts(file_name: str) -> dict:
    """

    :param file_name:
    :return:
    """
    with open(file_name, encoding="UTF-8") as file:
        return loads(file.read())
