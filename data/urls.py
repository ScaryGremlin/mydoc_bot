from dataclasses import dataclass


@dataclass
class Urls:
    iis_api_base: str = "http://mfc{}.lk.umfc26.ru/rest-api/"
    iis_api_case_status: str = "case/status"
    iis_api_cases_list: str = "case/list"
    iis_api_statuses_list: str = "case/list-status"
    iis_api_subdivisions_list: str = "subdivision/list"
    iis_api_feed_back_send: str = "feedback/send"
    iis_api_record_preliminary: str = "record/preliminary"
    iis_api_schedule_list: str = "schedule/list"
    iis_api_feedback: str = "feedback/send"
    google_maps: str = "https://www.google.com/maps/search/?api=1&query={lat}%2C{lon}"
