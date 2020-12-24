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
    

if __name__ == "__main__":
    text = 'погода в питере'
    main(text)
    
