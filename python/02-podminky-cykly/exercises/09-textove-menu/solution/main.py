loop = True
menu_text = f"""
{'*' * 20}
1 - spocitej samohlasky ve slove
2 - obrat poradi znaku slova
0 - kones
{'*' * 20}
"""

while loop:
    print(menu_text)
    user_input = input('Enter a choice: ').strip().lower()

    if user_input == '1':
        word = input('Enter a word: ').strip().lower()
        vowels_count = 0

        for letter in word:
            if letter in "aeiouy":
                vowels_count += 1

        print(f"Vowels count: {vowels_count}")

    elif user_input == '2':
        word = input('Enter a word: ').strip().lower()
        word_reversed = ""
        length = len(word)

        for index in range(length):
            word_reversed += word[length - index - 1]

        print(word_reversed)

    elif user_input == '0':
        loop = False

    else:
        print('Invalid input')
