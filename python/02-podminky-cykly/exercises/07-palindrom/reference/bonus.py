text = input("Zadej text: ")
cleaned = text.replace(" ", "").lower()

left = 0
right = len(cleaned) - 1
is_palindrome = True

while left < right:
    if cleaned[left] != cleaned[right]:
        is_palindrome = False
        break

    left += 1
    right -= 1

print("je palindrom" if is_palindrome else "není palindrom")
