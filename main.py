from colorama import init, Fore, Back, Style
import os, random, re

print('Loading...')

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

init(autoreset=True)

with open('words.txt') as f:
    words_list = [word[:-1].strip().lower() for word in f.readlines()]
    
with open('words_raw.txt') as f:
    guessable_words_list = [word[:-1].strip().lower() for word in f.readlines()]
    guessable_words_list.append('q')

# Magic function, idk i just copied of the diagram from wikipedia :P
# https://wikimedia.org/api/rest_v1/media/math/render/svg/efbf653f8a0a02b9e345f0070785893b5e7bcc16
def leven_dist(string1: str, string2: str) -> int:
    len1 = len(string1)
    len2 = len(string2)
    
    if len2 == 0:
        return len1
    elif len1 == 0:
        return len2
    elif string1[0] == string2[0]:
        return leven_dist(string1[1:], string2[1:])
    else:
        dist_tail1_2 = leven_dist(string1[1:], string2)
        dist_1_tail2 = leven_dist(string1, string2[1:])
        dist_tail1_tail2 = leven_dist(string1[1:], string2[1:])
        
        return 1 + min(dist_tail1_2, dist_1_tail2, dist_tail1_tail2)

def display_title() -> None:
    print(f'''
{Fore.CYAN}╔══════════════════╗
{Fore.CYAN}║                  ║
{Fore.CYAN}║{Fore.YELLOW}     WordLink{Fore.CYAN}     ║
{Fore.CYAN}║                  ║
{Fore.CYAN}╚══════════════════╝''')

clear()

display_title()
print(f'Press {Fore.YELLOW}Enter{Style.RESET_ALL} to start.')
input()

guessed_words: dict = {}

def display_guessed_words() -> None:
    for word, leven in guessed_words.items():
        color = None
        
        if leven <= 1:
            color = Fore.GREEN
        elif leven == 2:
            color = Fore.CYAN
        elif leven in [3, 4]:
            color = Fore.BLUE
        else:
            color = Style.DIM
        
        print(f'{color}{word}{Style.RESET_ALL} ({Fore.WHITE}{leven}{Style.RESET_ALL})')
        
def get_nearby_words(word: str, threshold: int=2) -> dict[str, int]:
    return_dict: dict = {}
    
    for possible_word in words_list:
        levendist = leven_dist(word, possible_word)
        if 0 < levendist <= threshold:
            return_dict[possible_word] = levendist
    
    return return_dict

print('Choosing starting word...')
print(f'{Style.DIM}This may take a while.')

answer_word: str = random.choice(words_list)
nearby_words = get_nearby_words(answer_word)

guessed_words = {pair[0]: pair[1] for pair in random.sample(list(nearby_words.items()), min(len(nearby_words), random.randint(2,4)))}
    
found_word: bool = False
input_word: str = None

while True:
    clear()
    
    display_title()
    print()
    display_guessed_words()
    print()
    
    print(f'{Fore.YELLOW}Enter a word!')
    print(f'Or, enter "q" to quit.')
    
    word_is_valid: bool = False
    
    while not word_is_valid:
        input_word = input(': ').strip().lower()
        
        if re.match('^[a-z]+$', input_word) and input_word in guessable_words_list:
            word_is_valid = True
        print(f'{Fore.RED}Word does not exist! (in English)')
    
    if input_word == 'q':
        clear()
        
        display_title()
        print()
        display_guessed_words()
        print(f'\nThe word was {Style.BRIGHT}{Fore.CYAN}{answer_word}{Style.RESET_ALL}.')
        print(f'{Style.DIM}Play again?')

        break
    elif input_word == answer_word:
        clear()
        
        display_title()
        print()
        display_guessed_words()
        print(f'\n{Fore.RED}Y{Fore.YELLOW}O{Fore.GREEN}U {Fore.CYAN}W{Fore.BLUE}I{Fore.MAGENTA}N{Fore.WHITE}!')
        print(f'The word was {Style.BRIGHT}{Fore.CYAN}{answer_word}{Style.RESET_ALL}!')
        print(f'{Style.DIM}Play again?')

        break
    else:
        guessed_words[input_word] = leven_dist(input_word, answer_word)
        
        guessed_words = dict(sorted(guessed_words.items(), key=lambda x: x[1]))
