text = input("Zadej text: ")

text_no_spaces = text.strip().replace(" ", "")

length = len(text_no_spaces)

idx_a = 0
idx_b = length - 1
is_palindrome = True

while idx_a < idx_b:
  char_a = text_no_spaces[idx_a].lower()
  char_b = text_no_spaces[idx_b].lower()

  if char_a != char_b:
    is_palindrome = False
    break

  idx_a += 1
  idx_b -= 1

result_message = 'je palindrom' if is_palindrome else 'neni palindrom'

print(f"{text}{result_message:.>20}")
