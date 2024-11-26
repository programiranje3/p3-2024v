from lab6.putnik import Putnik
from lab6.kategorije_putnika import PutnikEkonomskeKlase, PutnikBiznisKlase
from lab6.flight_enum import UslugaNaLetu
from datetime import datetime
from sys import stderr

class Let:

    poletanje_dt_format = '%Y-%m-%d %H:%M'

    def __init__(self, let, poletanje, ruta):
        self.broj_leta = let
        self.vreme_poletanja = poletanje
        self.ruta = ruta
        self.putnici = []


    @property
    def vreme_poletanja(self):
        # if not hasattr(self, '_Let__vreme_poletanja'):
        #     self.__vreme_poletanja = None
        # return self.__vreme_poletanja
        try:
            return self.__vreme_poletanja
        except AttributeError:
            self.__vreme_poletanja = None
            return self.__vreme_poletanja

    @vreme_poletanja.setter
    def vreme_poletanja(self, value):
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, Let.poletanje_dt_format)
            except ValueError as err:
                stderr.write(f"Greska! Format vremena poletanja ne odgovara ocekivanom ({Let.poletanje_dt_format})\n")
                return
        if isinstance(value, datetime) and value > datetime.now():
            self.__vreme_poletanja = value
        else:
            stderr.write(f"Greska! Nepoznat format za datum i vreme poletanja -> vrednost nije dodeljenja!\n")

    @property
    def ruta(self):
        try:
            return self.__ruta
        except AttributeError:
            self.__ruta = None
            return self.__ruta

    @ruta.setter
    def ruta(self, value):
        if isinstance(value, (list, tuple)) and len(value) == 2:
            self.__ruta = tuple(value)
            return
        if isinstance(value, str):
            import re
            try:
                origin, destination = re.split(",|-|>", value)
                self.__ruta = origin.strip(), destination.strip()
            except ValueError as err:
                stderr.write(f"Greska! Ruta nije u ocekivanom formatu\n")



    def dodaj_putnika(self, p):
        if not isinstance(p, Putnik):
            stderr.write(f"Greska! Pogresan tip ulaznog argumenta, ocekivan objekat klase Putnik, "
                         f"primljen objekat klase {type(p)}\n")
            return
        if p in self.putnici:
            stderr.write(f"Putnik {p.ime} ({p.pasos}) je vec u listi putnika\n")
            return
        if not p.COVID_bezbedan:
            stderr.write(f"Putnik {p.ime} ({p.pasos}) nema potvrdu da je COVID bezbedan\n")
            return

        self.putnici.append(p)


    def vreme_poletanja_str(self):
        return datetime.strftime(self.vreme_poletanja, Let.poletanje_dt_format) if self.vreme_poletanja else 'nepoznato'

    def ruta_str(self):
        if not self.ruta:
            return "nepoznata"
        origin, destination = self.ruta
        return f"{origin} => {destination}"

    def __str__(self):
        let_str = f"Let {self.broj_leta}\n"
        let_str += f"Datum i vreme poletanja: {self.vreme_poletanja_str()}\n"
        let_str += "Ruta: " + self.ruta_str() + "\n"
        if len(self.putnici) > 0:
            let_str += "Putnici na letu:\n" + '\n'.join([str(p) for p in self.putnici])
        else:
            let_str += "Let jos nema prijavljenih putnika"
        return let_str


    @classmethod
    def from_dict(cls, value_dict):
        # `br_leta`, `vreme_poletanja`, `polazna_lokacija`, `odrediste`
        try:
            return cls(value_dict['br_leta'], value_dict['vreme_poletanja'],
                       (value_dict['polazna_lokacija'], value_dict['odrediste']))
        except KeyError as err:
            stderr.write(f"Greska! Nepoznat kljuc: {err}\n")
            stderr.write("Let ce biti kreiran sa raspolozivim atributima: ")
            expected_labels = {"br_leta", "vreme_poletanja", "polazna_lokacija", "odrediste"}
            actual_lables = set(value_dict.keys())
            stderr.write(", ".join(expected_labels.intersection(actual_lables)) + "\n")

            def value_of(key):
                return value_dict[key] if key in value_dict.keys() else None

            return cls(value_of('br_leta'), value_of('vreme_poletanja'),
                      (value_of('polazna_lokacija'), value_of('odrediste')))



    def vreme_do_poletanja(self):
        if self.vreme_poletanja:
            dt = self.vreme_poletanja - datetime.now()
            days = dt.days
            hours, sec_remained = divmod(dt.seconds, 3600)
            mins = sec_remained // 60
            return days, hours, mins

        stderr.write("Greska! Vreme poletanja nije poznato!\n")
        return None


    def __iter__(self):
        self.__next_index = 0
        return self


    def __next__(self):
        if self.__next_index == len(self.putnici):
            raise StopIteration

        next = self.putnici[self.__next_index]
        self.__next_index += 1
        return next

    def generator_putnika_sa_uslugama(self):
        from collections import defaultdict
        service_dict = defaultdict(int)
        for putnik in self.putnici:
            if len(putnik.usluge) > 0:
                yield putnik
                for usluga in putnik.usluge:
                    service_dict[usluga] += 1

        print(f"\nSumarni pregled dodatnih usluga za let {self.broj_leta}:")
        for usluga, frekv in sorted(service_dict.items(), key=lambda item: item[1], reverse=True):
                print(f"{usluga}: {frekv}")


    def generator_kandidata_za_biznis_klasu(self, prag_za_biznis_klasu):
        kandidati = []
        for putnik in self.putnici:
            if (isinstance(putnik, PutnikEkonomskeKlase) and
                    len(putnik.usluge) > 0 and
                    putnik.cena_karte > prag_za_biznis_klasu):
                kandidati.append(putnik)
        for putnik in sorted(kandidati, key=lambda p: p.cena_karte, reverse=True):
            yield putnik




if __name__ == '__main__':

    lh1411 = Let('LH1411', '2024-12-20 6:50', ('Belgrade', 'Munich'))
    print(lh1411)
    print()

    lh992 = Let('LH992', '2024-12-25 12:20', 'Belgrade > Frankfurt')
    print(lh992)
    print()

    lh1514_dict = {'br_leta':'lh1514',
                   'vreme_poletanja': '2025-1-9 16:30',
                   'polazna_lokacija': 'Paris',
                   'odrediste': 'Berlin'}

    lh1514 = Let.from_dict(lh1514_dict)
    print(lh1514)
    print()

    bob = PutnikEkonomskeKlase("Bob Smith", "UK", "123456", 250.0, True)
    john = PutnikEkonomskeKlase("John Smith", "USA", 987656, 450, True)
    luis = PutnikBiznisKlase(ime_prezime="Luis Bouve", drzava='France', pasos="123654", cena_karte=225,
                             usluge_na_letu=[UslugaNaLetu.OBROK, UslugaNaLetu.WIFI], COVID_bezbedan=True)

    anna = PutnikEkonomskeKlase("Anna Smith", "Spain", "987659", 375, True)
    try:
        dodatne_usluge = {UslugaNaLetu.OBROK: 10, UslugaNaLetu.WIFI: 15}
        anna.dodaj_izabrane_usluge(dodatne_usluge)
    except ValueError as err:
        stderr.write(f"Iz dodaj_izabrane_usluge: Greska! {err}")


    print(f"\nDodavanje putnika na let {lh1411.broj_leta}")
    for p in [bob, john, anna, luis]:
        lh1411.dodaj_putnika(p)

    print(f"\nPodaci o letu {lh1411.broj_leta} nakon dodavanja putnika na let:\n")
    print(lh1411)

    print("\nPutnici sa dodatnim uslugama na letu:")
    g = lh1411.generator_putnika_sa_uslugama()
    while True:
        try:
            print(next(g))
        except StopIteration:
            print("------- kraj spiska putnika sa dodatnim uslugama --------")
            break

    # for putnik in lh1411.generator_putnika_sa_uslugama():
    #     print(putnik)

    # Dodacemo putnicima usluge na letu radi provere generatorske metode
    try:
        dodatne_usluge_bob = {UslugaNaLetu.IZBOR_SEDISTA: 20, UslugaNaLetu.OSIGURANJE_LETA: 35}
        bob.dodaj_izabrane_usluge(dodatne_usluge_bob)
    except ValueError as err:
        stderr.write(f"Iz dodaj_izabrane_usluge: Greska! {err}")

    try:
        dodatne_usluge_john = {UslugaNaLetu.OBROK: 20, UslugaNaLetu.WIFI: 35}
        john.dodaj_izabrane_usluge(dodatne_usluge_john)
    except ValueError as err:
        stderr.write(f"Iz dodaj_izabrane_usluge: Greska! {err}")

    print()
    print("Kandidati za prelazak u biznis klasu:")
    g = lh1411.generator_kandidata_za_biznis_klasu(350)
    try:
        while True:
            print(next(g))
    except StopIteration:
        print("--- kraj liste kandidata ---")

    # print("\nPutnici kojima je ponudjena mogucnost prelaska u biznis klasu:")
    # for ind, putnik in enumerate(lh1411.generator_kandidata_za_biznis_klasu(350)):
    #     print(f"{ind+1}. {putnik}")


