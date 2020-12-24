from src.skills.utils import get_tokens
from src.skills.slot import Slot

class GetWeatherSkill:

    LOCATION = 'location'
    DATE = 'date'

    def __init__(self, slots):
        self.params = dict()
        self._is_complete = False
        self._is_run = False
        self.slots = slots

    def feed(self, text):
        if self._is_complete:
            return self._is_complete, None

        tokens = get_tokens(text)

        extracted_location, query = self.extract_location(tokens)
        if query:
            return False, query

        extracted_date, query = self.extract_date(tokens)
        if query:
            return False, query
            
        is_complete = extracted_location and extracted_date
        query_text = None
        if not is_complete:
            query_text = self.choose_query()
            
        self._is_complete = is_complete
        
        return self._is_complete, query_text


    def is_complete(self) -> bool:
        return self._is_complete


    def is_run(self) -> bool:
        return self._is_run


    def run(self):
        if not self._is_complete:
            raise Exception("Собраны не все параметры")

        self._is_run = True
        return f"Прогноз погоды для города {self.params[GetWeatherSkill.LOCATION]} на {self.params[GetWeatherSkill.DATE]}"


    def extract_date(self, lemmas):
        if self.params.get(GetWeatherSkill.DATE):
            return True, None

        dates = set()

        for slot in self.slots[GetWeatherSkill.DATE].values():
            intersection = lemmas & slot.aliases
            if len(intersection) > 0:
                dates.add(slot.id)

        if len(dates) > 1:
            return False, 'Пожалуйста, укажите одну дату'

        if len(dates) == 1:
            self.params[GetWeatherSkill.DATE] = list(dates)[0]
            return True, None
        else:
            return False, None


    def extract_location(self, lemmas):
        if self.params.get(GetWeatherSkill.LOCATION):
            return True, None

        locations = set()

        for slot in self.slots[GetWeatherSkill.LOCATION].values():
            intersection = lemmas & slot.aliases
            if len(intersection) > 0:
                locations.add(slot.id)

        if len(locations) > 1:
            return False, 'Пожалуйста, укажите один город'

        if len(locations) == 1:
            self.params[GetWeatherSkill.LOCATION] = list(locations)[0]
            return True, None
        else:
            return False, None


    def choose_query(self):
        if not self.params.get(GetWeatherSkill.LOCATION):
            return "В каком городе?"

        if not self.params.get(GetWeatherSkill.DATE):
            return "На какой день смотреть погоду?"


class GetWeatherSkillSlots:

    SLOTS = {
        'location': {
            'spb': Slot('spb', 'Санкт-Петербург', { "спб", "питер", "петербург", "санкт-петербург" }),
            'moscow': Slot('moscow', 'Москва', { "мск", "москва" }),
        },
        'date': {
            'today': Slot('today', 'сегодня', { "сегодня" })
        }
    }