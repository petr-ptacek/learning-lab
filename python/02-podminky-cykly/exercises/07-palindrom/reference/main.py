text = input("Zadej text: ")

left = 0
right = len(text) - 1
is_palindrome = True

while left < right:
    if text[left].lower() != text[right].lower():
        is_palindrome = False
        break

    left += 1
    right -= 1

print(f'"{text}" {"je" if is_palindrome else "není"} palindrom')
