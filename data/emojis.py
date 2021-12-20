from dataclasses import dataclass

from emoji import emojize


@dataclass
class Emoji:
    clipboard: str = emojize(":clipboard:")
    office_building: str = emojize(":office_building:")
    round_pushpin: str = emojize(":round_pushpin:")
    slightly_smiling_face: str = emojize(":slightly_smiling_face:")
    frowning_face: str = emojize(":frowning_face:")
    thinking_face: str = emojize(":thinking_face:")
    red_question_mark: str = emojize(":red_question_mark:")
    cross_mark: str = emojize(":cross_mark:")
    right_arrow_curving_left: str = emojize(":right_arrow_curving_left:")
    world_map: str = emojize(":world_map:")
    five_o_clock: str = emojize(":five_o’clock:")
    home: str = emojize(":house:")
    card_index_dividers: str = emojize(":card_index_dividers:")
    robot: str = emojize(":robot:")
    check_mark: str = emojize(":check_mark:")
    warning: str = emojize(":warning:")
    technologist: str = emojize(":technologist:")
    stop_sign: str = emojize(":stop_sign:")
    mobile_phone: str = emojize(":mobile_phone:")
