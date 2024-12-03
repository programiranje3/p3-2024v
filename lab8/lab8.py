from pathlib import Path
from sys import stderr
import pickle
import json
from pprint import pprint

DATA_DIR = Path.cwd() / 'data'

def get_results_dir():
    results_dir = Path.cwd() / 'results'
    if not results_dir.exists():
        results_dir.mkdir(parents=True)
    return results_dir


def ucitaj_iz_txt_fajla(fpath):
    txt = None
    try:
        with open(fpath, 'r') as fobj:
            txt = [line.rstrip('\n') for line in fobj.readlines()]
    except FileNotFoundError:
        stderr.write(f"Greska pri ucitavanju iz fajla '{fpath}' - zadati fajl ne postoji!\n")
    except OSError as err:
        stderr.write(f"Greska pri ucitavanju iz fajla '{fpath}':\n{err}\n")
    finally:
        return txt


def upisi_u_txt_fajl(txt_as_list, fpath):
    try:
        with open(fpath, 'w') as fobj:
            for line in txt_as_list:
                fobj.write(line + "\n")
    except OSError as err:
        stderr.write(f"Greska pri upisivanju teksta u fajl '{fpath}':\n{err}\n")


def serijalizuj_podatke(data, fpath):
    try:
        with open(fpath, "wb") as fobj:
            pickle.dump(data, fobj)
    except pickle.PicklingError as err:
        stderr.write(f"Greska pri serijalizaciji podataka:\n{err}\n")
    except OSError as err:
        stderr.write(f"Greska pri pristupu fajlu '{fpath}' radi serijalizaciji podataka:\n{err}\n")


def deserijalizuj_podatke(fpath):
    data = None
    try:
        with open(fpath, "rb") as fobj:
            data = pickle.load(fobj)
    except pickle.UnpicklingError as err:
        stderr.write(f"Greska pri deserijalizaciji podataka:\n{err}\n")
    except OSError as err:
        stderr.write(f"Greska pri pristupu fajlu '{fpath}' radi deserijalizacije podataka:\n{err}\n")
    finally:
        return data


def upisi_u_json(data, fpath):
    try:
        with open(fpath, "w") as fobj:
            json.dump(data, fobj, indent=4)
    except OSError as err:
        stderr.write(f"Greska pri pristupu fajlu '{fpath}' radi upisa podataka:\n{err}\n")


def ucitaj_iz_jsona(fpath):
    try:
        with open(fpath, "r") as fobj:
            return json.load(fobj)
    except OSError as err:
        stderr.write(f"Greska pri pristupu fajlu '{fpath}' radi ucitavanja podataka:\n{err}\n")
        return None


def analiza_fajlova_sa_slikama(fpath):
    from collections import defaultdict

    img_dict = defaultdict(list)

    for line in ucitaj_iz_txt_fajla(fpath):
        dir_path, fname = line.rsplit('/', maxsplit=1)
        _, _, dir_category = dir_path.split('/', maxsplit=2)
        dir_category = dir_category.replace("/", "_")
        img_dict[dir_category].append(fname)

    for_txt_file = []
    for img_category, img_list in img_dict.items():
        for_txt_file.append(f"{img_category}: {len(img_list)}")

    upisi_u_txt_fajl(for_txt_file, get_results_dir() / 'zadatak1_stats.txt')

    serijalizuj_podatke(img_dict, get_results_dir() / 'zadatak1_dict.pkl')


def unos_podataka_o_timu():

    prompt = """
        Unesite podatke o clanovima tima u sledecem obliku:
        ime_prezime, godine_starosti, osvojeni_poeni
        Za prekid unosa, unesite 'kraj'
    """
    print(prompt)

    members_data = []

    done = False
    while not done:
        data = input()
        if data.lower() == 'kraj':
            done = True
        else:
            try:
                name, age, score = data.split(',')
                members_data.append({
                    'name': name,
                    'age': int(age.strip()),
                    'score': float(score.strip())
                })
            except ValueError as err:
                stderr.write(f"Greska pri procesiranju unosa: '{data}': {err}\n")
                print("Greska! Probajte ponovo")


    members_data.sort(key=lambda member: member['score'], reverse=True)

    upisi_u_json(members_data, get_results_dir() / 'zadatak2_clanovi_tima.json')


def zabelezi_presek_brojeva(fpath1, fpath2):

    fdata1 = ucitaj_iz_txt_fajla(fpath1)
    fdata2 = ucitaj_iz_txt_fajla(fpath2)
    if not (fdata1 and fdata2):
        raise RuntimeError("Nije moguce ucitati podatke iz nekog od izvornih fajlova => funkcija ne moze da nastavi sa radom")

    num1 = [int(item) for item in fdata1 if item != "" and item.isdigit()]
    num2 = [int(item) for item in fdata2 if item != "" and item.isdigit()]
    num3 = list(set(num1).intersection(set(num2)))

    def get_stats_dict(l):
        from statistics import mean, stdev
        return {
            'N': len(l),
            'M': mean(l),
            'SD': stdev(l)
        }

    for_json_file = [get_stats_dict(num1), get_stats_dict(num2), get_stats_dict(num3)]
    upisi_u_json(for_json_file, get_results_dir() / 'zadatak3_statistike.json')


if __name__ == '__main__':

    # Zadatak 1
    # analiza_fajlova_sa_slikama(DATA_DIR / 'image_files_for_training.txt')
    #
    # zad1_recnik = deserijalizuj_podatke(get_results_dir() / 'zadatak1_dict.pkl')
    # if zad1_recnik:
    #     for ent, lista_slika in zad1_recnik.items():
    #         print(f"{ent.upper()}: {', '.join(lista_slika)}")

    # zad1_lista = ucitaj_iz_txt_fajla(get_results_dir() / 'zadatak1_stats.txt')
    # if zad1_lista:
    #     for entity_stat in zad1_lista:
    #         print(entity_stat)

    #
    # # Zadatak 2
    # unos_podataka_o_timu()
    #
    # podaci_o_clanovima = ucitaj_iz_jsona(get_results_dir() / 'zadatak2_clanovi_tima.json')
    # if podaci_o_clanovima:
    #     for podaci_o_clanu in podaci_o_clanovima:
    #         ime, godine, poeni = podaci_o_clanu.values()
    #         print(f"{ime}, {godine} godine, {poeni} poena")
    #
    #
    # Zadatak 3
    f1 = DATA_DIR / 'happy_numbers.txt'
    f2 = DATA_DIR / 'prime_numbers.txt'
    try:
        zabelezi_presek_brojeva(f1, f2)
    except RuntimeError as err:
        stderr.write(str(err))
    else:
        zad1_recnik = ucitaj_iz_jsona(get_results_dir() / 'zadatak3_statistike.json')
        pprint(zad1_recnik)