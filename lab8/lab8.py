
if __name__ == '__main__':

    pass

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
    # f1 = DATA_DIR / 'happy_numbers.txt'
    # f2 = DATA_DIR / 'prime_numbers.txt'
    # try:
    #     zabelezi_presek_brojeva(f1, f2)
    # except RuntimeError as err:
    #     stderr.write(str(err))
    # else:
    #     zad1_recnik = ucitaj_iz_jsona(get_results_dir() / 'zadatak3_statistike.json')
    #     pprint(zad1_recnik)