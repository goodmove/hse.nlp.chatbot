from src.skills.get_weather import GetWeatherSkill
from src.skills.slot import Slot

slots = {
    'location': {
        'spb': Slot('spb', 'Санкт-Петербург', { "спб", "питер", "петербург", "санкт-петербург" }),
        'moscow': Slot('moscow', 'Москва', { "мск", "москва" }),
    },
    'date': {
        'today': Slot('today', 'сегодня', { "сегодня" })
    }
}

skill = GetWeatherSkill(slots)

def main(text):
    print("Ready")

    query_text = ''
    while not skill.complete():
        text = input(query_text)
        if len(text) > 0:
            is_complete, query = skill.feed(text)

            if not is_complete:
                query_text = f'{query}\n'

    print(skill.run())
    

import re
if __name__ == "__main__":
    text = 'погода в питере 12 марта'
    pattern = r'\d\d? [а-яА-Я]+'
    matches = re.findall(pattern, text.lower())
    print(matches)
    # main(text)
    
