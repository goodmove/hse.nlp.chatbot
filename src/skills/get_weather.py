from src.skills.utils import get_tokens, lemmatize
from src.skills.slot import Slot
import re
from datetime import datetime


class DateParam:

    def __init__(self, id: str, value: str):
        self.id = id
        self.value = value


class LocationParam:

    def __init__(self, id: str, value: str):
        self.id = id
        self.value = value



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

        extracted_date, query = self.extract_date(text, tokens)
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

        date = self.date_param_to_date(self.params[GetWeatherSkill.DATE])
        location = self.params[GetWeatherSkill.LOCATION].value

        self._is_run = True
        return f"Прогноз погоды для города {location} на {date}"


    def extract_date(self, text: str, lemmas):
        if self.params.get(GetWeatherSkill.DATE):
            return True, None

        dates = set()

        for slot in self.slots[GetWeatherSkill.DATE].values():
            if slot.pattern:
                matches = re.findall(slot.pattern, text.lower())
                for match_value in matches:
                    date_value = self.parse_date_match(match_value)
                    if date_value:
                        dates.add(DateParam(slot.id, date_value))

            else:
                intersection = lemmas & slot.aliases
                if len(intersection) > 0:
                    dates.add(DateParam(slot.id, slot.name))

        if len(dates) > 1:
            return False, 'Пожалуйста, укажите одну дату'

        if len(dates) == 1:
            self.params[GetWeatherSkill.DATE] = list(dates)[0]
            return True, None
        else:
            return False, None


    def parse_date_match(self, match_value):
        values = match_value.split(' ')
        day = int(values[0])
        month = lemmatize(values[1].lower())

        if not month or month not in GetWeatherSkillSlots.MONTHS.values():
            return None

        now = datetime.now()
        current_month = now.month
        year = now.year
        month_id = GetWeatherSkillSlots.MONTHS_REVERSE[month]

        if month_id < current_month:
            year += 1

        date = f'{year}/{month_id}/{day}'
        print(date)
        return date


    def date_param_to_date(self, date_param: DateParam):
        now = datetime.now()

        if date_param.id == 'pattern':
            return date_param.value

        elif date_param.id == 'today':
            return f'{now.year}/{now.month}/{now.day}'

        elif date_param.id == 'today+1':
            return f'{now.year}/{now.month}/{now.day+1}'

        elif date_param.id == 'today+2':
            return f'{now.year}/{now.month}/{now.day+2}'

        else:
            raise Exception(f'Unknown date id: {date_param.id}')


    def extract_location(self, lemmas):
        if self.params.get(GetWeatherSkill.LOCATION):
            return True, None

        locations = set()

        for slot in self.slots[GetWeatherSkill.LOCATION].values():
            intersection = lemmas & slot.aliases
            if len(intersection) > 0:
                locations.add(LocationParam(slot.id, slot.name))

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
            'today': Slot('today', 'сегодня', { "сегодня" }),
            'today+1': Slot('today+1', 'завтра', { "завтра" }),
            'today+2': Slot('today+2', 'послезавтра', { "послезавтра" }),
            'pattern': Slot('pattern', '', {}, pattern=r'\d\d? [а-яА-Я]+')
        }
    }


    MONTHS = { 1: 'январь', 2: 'февраль', 3: "март", 4: "апрель", 5: "май", 6: "июнь", 7: "июль", 8: "август", 9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь" }
    MONTHS_REVERSE = dict([(v, k) for k, v in MONTHS.items()])



