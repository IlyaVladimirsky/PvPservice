class MatchLogic:
    def __init__(self):
        pass

    def create_match_request(self, nickname, ip):
        response = {
            'nickname': nickname,
            'ip': ip
        }
        return response

    def get_error_message(self, text):
        return {'error': text}
