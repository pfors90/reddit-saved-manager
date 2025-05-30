import configparser

class Config:
    def __init__(self, config_file):
        self._parser = configparser.ConfigParser()
        with open(config_file) as f:
            self._parser.read_file(f)

    @property
    def DATABASE_PATH(self):
        return self._parser['DATABASE']['DATABASE_PATH']

    @property
    def API_KEY(self):
        return self._parser['AUTH']['API_KEY']

    @property
    def CLIENT_ID(self):
        return self._parser['AUTH']['CLIENT_ID']

    @property
    def CLIENT_SECRET(self):
        return self._parser['AUTH']['CLIENT_SECRET']

    @property
    def USER_AGENT(self):
        return self._parser['AUTH']['USER_AGENT']

    @property
    def USERNAME(self):
        return self._parser['AUTH']['USERNAME']

    @property
    def PASSWORD(self):
        if self.IS_2FA == 1:
            auth_code = str(input("Enter 2FA code: "))
            return self._parser['AUTH']['PASSWORD'] + ":" + auth_code
        return self._parser['AUTH']['PASSWORD']

    @property
    def IS_2FA(self):
        return int(self._parser['AUTH']['IS_2FA'])