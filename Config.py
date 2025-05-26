import configparser

# why was this included?
# from http.cookiejar import offset_from_tz_string

# TODO -----
# rewrite this class to not use an .ini file but rather
# just directly store all necessary information in this
# class file and have the user edit as needed
#
# this will allow for easier storing and retrieval of refresh
# tokens to avoid having to update 2FA codes and re-request auth
#
# api_caller.auth() can be modified to request and store all of
# this info at first launch?

# store reddit instance in Config class to avoid passing around?

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
        return self._parser['AUTH']['IS_2FA']