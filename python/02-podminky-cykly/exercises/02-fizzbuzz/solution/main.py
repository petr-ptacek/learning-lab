num = int(input("Enter a number: "))

score1 = int(input("Enter a target number: "))
song1 = input("Enter a song name: ")

score2 = int(input("Enter a target number: "))
song2 = input("Enter a song name: ")

for n in range(1, num + 1):
  message = f"{n}"

  if n % score1 == 0 and n % score2 == 0:
    message = song1 + song2
  elif n % score1 == 0:
    message = song1
  elif not bool(n % score2):
    message = song2

  print(message)
