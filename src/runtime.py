from src.intent.constants import IntentEnum
from src.skills.get_weather import GetWeatherSkill, GetWeatherSkillSlots

class State:
    def __init__(self, user_id, text):
        self.user_id = user_id
        self.intent = None
        self.prev_text = None
        self.cur_text = text
        self.skill = None

    def reset(self):
        self.prev_text = self.cur_text
        self.cur_text = None
        self.intent = None
        self.skill = None

    
    def shift(self, text):
        self.prev_text = self.cur_text
        self.cur_text = text


class Runtime:

    def __init__(self, classifier):
        self.states = dict()
        self.classifier = classifier


    def run(self, user_id, text) -> str:
        user_state: State = self.states.get(user_id)
        if not user_state:
            user_state = State(user_id, text)
            self.states[user_id] = user_state
        else:
            user_state.shift(text)


        if user_state.skill and not user_state.skill.is_run():
            return self.feed_skill(user_state)

        else:
            state, response = self.parse_intent_and_reply(user_state)
            self.post_process_intent(state)

            return response


    def feed_skill(self, user_state: State):
        response = None
        is_complete, query = user_state.skill.feed(user_state.cur_text)

        if is_complete:
            response = user_state.skill.run()
        else:
            response = query

        return response

        
    def parse_intent_and_reply(self, user_state: State) -> str:
        intent_class = self.classifier.classify(user_state.cur_text)

        if intent_class is None:
            return user_state, 'Что-то я не понял.. Попробуй сказать по-другому'

        if intent_class == IntentEnum.GET_WEATHER:
            skill = GetWeatherSkill(GetWeatherSkillSlots.SLOTS)
            user_state.skill = skill
            response = self.feed_skill(user_state)

            return user_state, response
        
        elif intent_class == IntentEnum.GREETING:
            user_state.reset()

            return user_state, "Привет!"

        elif intent_class == IntentEnum.GOODBYE:
            user_state.reset()

            return user_state, "До встречи)"
        else:
            return user_state, "Я совсем запутался :("

    
    def post_process_intent(self, user_state: State):
        if user_state.intent == IntentEnum.GOODBYE:
            del self.states[user_state.user_id]
