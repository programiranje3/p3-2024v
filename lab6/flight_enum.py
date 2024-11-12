from enum import Enum

class UslugaNaLetu(Enum):

    # izbor sedista, obrok, wifi, osiguranje leta, prioritetno ukrcavanje
    IZBOR_SEDISTA = 'izbor sedista'
    OBROK = 'obrok'
    WIFI = 'wifi'
    OSIGURANJE_LETA = 'osiguranje leta'
    PRIORITETNO_UKRCAVANJE = 'prioritetno ukrcavanje'

    @staticmethod
    def valid_service_str(service_string):
        for service in UslugaNaLetu:
            if service.value.lower() == service_string.lower():
                return True
        return False


    @staticmethod
    def get_service_from_str(service_string):
        if not UslugaNaLetu.valid_service_str(service_string):
            return None

        service_string = service_string.lower()
        for service in UslugaNaLetu:
            if service.name.lower() == service_string or service.value.lower() == service_string:
                return service



if __name__ == '__main__':

    print(UslugaNaLetu.valid_service_str('wifi'))

    print(UslugaNaLetu.valid_service_str('onboard wifi'))

    print(UslugaNaLetu.valid_service_str('izbor sedista'))

    print(UslugaNaLetu.get_service_from_str('izbor sedista'))
