"""
Vezbe, dvocas 3
"""
from collections import defaultdict

#%%
# Zadatak 1
def create_print_numeric_dict(n):
    d = dict()
    # Option 1
    # for x in range(1, n+1):
    #     d[x] = sum(range(x+1))
    # Option 2
    s = 0
    for x in range(1, n+1):
        s += x
        d[x] = s
    for key, val in sorted(d.items(), reverse=True):
        print(f"{key}: " + "+".join([str(i) for i in range(1,key+1)]) + f"={val}")

#%%
create_print_numeric_dict(7)

#%%
# Zadatak 2
def lists_to_dict(l1, l2):
    from operator import itemgetter
    d = dict()
    for item1, item2 in zip(l1, l2):
        d[item1] = item2
    for key, val in sorted(d.items(), key=itemgetter(1)):
        print(f"{key}: {val}")


#%%
dishes = ["pizza", "sauerkraut", "paella", "hamburger"]
countries = ["Italy", "Germany", "Spain", "USA", "Serbia"]
lists_to_dict(countries, dishes)

#%%
# Zadatak 3
def string_stats(string):
    # Option 1
    # stats_dict = {
    #     'digits':0,
    #     'letters':0,
    #     'punct_marks':0
    # }
    # Option 2
    stats_dict = defaultdict(int)
    for ch in string:
        if ch.isdigit():
            stats_dict['digits'] += 1
        elif ch.isalpha():
            stats_dict['letters'] += 1
        elif ch in '.,!?;:':
            stats_dict['punct_marks'] += 1
    return dict(stats_dict)


#%%
print("string_stats('Today is October 22, 2024!'):")
print(string_stats("Today is October 22, 2024!"))

#%%
# Zadatak 4
def password_check(passwords_to_verify):
    validity_check_dict = defaultdict(list)
    for pass_candidate in [p.strip() for p in passwords_to_verify.split(",")]:
        if len(pass_candidate) < 6 or len(pass_candidate) > 12:
            validity_check_dict[pass_candidate].append("inadequate length")
        if not any([ch.islower() for ch in pass_candidate]):
            validity_check_dict[pass_candidate].append("no lower case letters")
        if not any([ch.isupper() for ch in pass_candidate]):
            validity_check_dict[pass_candidate].append("no upper case letters")
        if not any([ch.isdigit() for ch in pass_candidate]):
            validity_check_dict[pass_candidate].append("no digits")
        if not any([ch in '$#@' for ch in pass_candidate]):
            validity_check_dict[pass_candidate].append("no special characters")
        if len(validity_check_dict[pass_candidate]) == 0:
            validity_check_dict[pass_candidate].append('valid')
    return dict(validity_check_dict)


#%%
print("Passwords to check: ABd1234@1, a F1#, 2w3E*, 2We334#5, t_456wr")
validation_dict = password_check("ABd1234@1, a F1#,2w3E*,2We334#5, t_456wr")
print("Validation results:")
for password, result in validation_dict.items():
    print(f"- {password}: {', '.join(result)}")

#%%
# Zadatak 5
def team_stats(team_data):
    from statistics import mean
    from operator import itemgetter

    mean_age = mean([mem_dict['age'] for mem_dict in team_data])
    print(f"Prosek godina clanova tima: {mean_age:.2f}")

    min_score_young_player = min([mem_dict for mem_dict in team_data if mem_dict['age'] < 21],
                                 key=itemgetter('score'))
    print(f"Najnizi skor medju igracima mladjim od 21 god ostvario je: {min_score_young_player['name']}")

    max_score_young_player = max([mem_dict for mem_dict in team_data if mem_dict['age'] < 21],
                                 key = itemgetter('score'))
    print(f"Najvisi skor medju igracima mladjim od 21 god ostvario je: {max_score_young_player['name']}")

    print("Svi clanovi tima:")
    for mem_dict in sorted(team_data, key=itemgetter('score'), reverse=True):
        name, age, score = mem_dict.values()
        print(f"{name} ({age}), scored: {score}")

#%%
team = [{'name': 'Bob', 'age': 18, 'score': 50.0},
        {'name': 'Tim', 'age': 17, 'score': 84.0},
        {'name': 'Jim', 'age': 22, 'score': 94.0},
        {'name': 'Joe', 'age': 19, 'score': 85.5}]
team_stats(team)

#%%
# Zadatak 6
# Napomena: za vise informacija o specificnostima sortiranja, pogledati:
# https://docs.python.org/3/howto/sorting.html#sort-stability-and-complex-sorts

def token_frequency(text):
    from collections import defaultdict

    tokens = text.split()

    freq_dict = defaultdict(int)
    for token in tokens:
        token = token.rstrip(',.;:!? ')
        if len(token) >= 3:
            freq_dict[token.lower()] += 1

    # print("Printing dictionary sorted alphabetically in ascending order of keys")
    # for token, freq in sorted(freq_dict.items()):
    #     print(f"{token}: {freq}")
    # print()

    from operator import itemgetter
    for token, freq in sorted(sorted(freq_dict.items()), key=itemgetter(1), reverse=True):
        print(f"{token}: {freq}")


#%%
# response by GPT-3 to the question of why it has so entranced the tech community
# source: https://www.wired.com/story/ai-text-generator-gpt-3-learning-language-fitfully/
# gpt3_response = ("""
#     I spoke with a very special person whose name is not relevant at this time,
#     and what they told me was that my framework was perfect. If I remember correctly,
#     they said it was like releasing a tiger into the world.
# """)
# token_frequency(gpt3_response)

short_text = "Here, here, we are now here"
token_frequency(short_text)

#%%
# Zadatak 7

def class_stats(class_size_data):
    from operator import itemgetter
    # Option 1
    # d = defaultdict(int)
    # for class_id, class_size in class_size_data:
    #     d[class_id] += class_size
    # for class_id, class_tot_size in sorted(d.items(), key=itemgetter(1), reverse=True):
    #     print(f"{class_id}: {class_tot_size}")
    # Option 2
    from collections import Counter
    classes = list()
    for class_id, class_size in class_size_data:
        classes.extend([class_id]*class_size)
    for class_id, class_tot_size in sorted(Counter(classes).items(), key=itemgetter(1), reverse=True):
        print(f"{class_id}: {class_tot_size}")


#%%
l = [('V', 1), ('VI', 1), ('V', 2), ('VI', 2), ('VI', 3), ('VII', 1)]
class_stats(l)

#%%
# Zadatak 8

def website_stats(websites_list):
    stats_dict = defaultdict(int)
    for ws in websites_list:
        _, suffix = ws.rsplit('.', maxsplit=1)
        suffix = suffix.rstrip('/')
        stats_dict[suffix] += 1
    return dict(stats_dict)


#%%
sample_websites = ['https://www.technologyreview.com/', 'https://www.tidymodels.org/',
                   'https://podcasts.google.com/', 'https://www.jamovi.org/', 'http://bg.ac.rs/']

print(website_stats(sample_websites))





