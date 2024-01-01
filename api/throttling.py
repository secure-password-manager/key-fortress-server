from rest_framework.throttling import AnonRateThrottle


class SignupAnonRateThrottle(AnonRateThrottle):

    def __init__(self):
        self.rate = '5/day'
        super().__init__()
