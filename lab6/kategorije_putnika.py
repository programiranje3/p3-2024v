from lab6.putnik import Putnik
from lab6.flight_enum import UslugaNaLetu

from sys import stderr

class PutnikEkonomskeKlase(Putnik):

    def dodaj_izabrane_usluge(self, recnik_usluge_i_cene):
        if not self.cena_karte or self.cena_karte == 0:
            raise ValueError(f"Greska! Karta za putnika {self.ime} ({self.pasos}) jos nije placena\n")

        dodatne_usluge = []
        uvecanje_cene = 0
        for usluga, cena in recnik_usluge_i_cene.items():
            if type(usluga) is UslugaNaLetu:
                dodatne_usluge.append(usluga)
                uvecanje_cene += cena

        self.cena_karte += uvecanje_cene
        self.usluge.extend(dodatne_usluge)

        print(f"Putnik {self.ime} ({self.pasos}) je uplatio sledece dodatne usluge: {', '.join([usluga.value for usluga in dodatne_usluge])}")
        print(f"Cena karte putnika je time uvecana za {uvecanje_cene} i iznosi {self.cena_karte}")

    def __str__(self):
        putnik_str = super().__str__()
        return putnik_str.replace("Putnik", "Putnik ekonomske klase")


class PutnikBiznisKlase(Putnik):

    def __init__(self, usluge_na_letu=(UslugaNaLetu.PRIORITETNO_UKRCAVANJE,), **kwargs):
        super().__init__(**kwargs)

        for usluga in usluge_na_letu:
            if isinstance(usluga, UslugaNaLetu):
                self.usluge.append(usluga)
            elif isinstance(usluga, str) and UslugaNaLetu.valid_service_str(usluga):
                self.usluge.append(UslugaNaLetu.get_service_from_str(usluga))
            else:
                stderr.write(f"Greska! Neadekvatna vrednost ({usluga}) za uslugu na letu\n")



    def __str__(self):
        return super().__str__().replace("Putnik", "Putnik biznis klase")



if __name__ == '__main__':

    jim = PutnikEkonomskeKlase("Jim Jonas", 'UK', '123456', 450, True)
    print(jim)
    print()

    # Add extra services to Jim
    extra_services = {
        UslugaNaLetu.OBROK: 10,
        UslugaNaLetu.WIFI: 15
    }
    try:
        jim.dodaj_izabrane_usluge(extra_services)
    except ValueError as err:
        stderr.write(f"Iz dodaj_izabrane_usluge: Greska! {err}")
    print(f"\nPutnik {jim.ime} nakon dodavanja usluga:")
    print(jim)
    print()

    bob = PutnikEkonomskeKlase("Bob Jones", 'Denmark', '987654', 420)
    print(bob)
    print()

    mike = PutnikBiznisKlase(ime_prezime="Mike Stone", drzava="USA",
                             pasos='234567', cena_karte=550, COVID_bezbedan=True,
                             usluge_na_letu=(UslugaNaLetu.PRIORITETNO_UKRCAVANJE, UslugaNaLetu.WIFI))
    print(mike)
    print()

    brian = PutnikBiznisKlase(ime_prezime="Brian Brown", drzava="UK",
                              pasos='546234', cena_karte=670, COVID_bezbedan=True,
                              usluge_na_letu=("Osiguranje leta", "Uzina", "Izbor sedista"))
    print(brian)


