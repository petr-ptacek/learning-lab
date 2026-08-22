num_a = float(input("Zadej stranu a: "))
num_b = float(input("Zadej stranu b: "))
num_c = float(input("Zadej stranu c: "))

can_build_triangle = num_b + num_c > num_a and num_a + num_c > num_b and num_a + num_b > num_c

if not can_build_triangle:
  print("Trojúhelnik nelze sestavit")
  exit(0)

tringle_type = ""
is_equilateral = False
is_isosceles = False
is_common = False

is_rectangular = False

if num_a == num_b == num_c:
  is_equilateral = True
  tringle_type = "rovnostranny"
elif num_a == num_b or num_a == num_c or num_b == num_c:
  is_isosceles = True
  tringle_type = "rovnoramenny"
else:
  is_common = True
  tringle_type = "obecny"

  if num_c > num_a and num_c > num_b:
    is_rectangular = num_c ** 2 == num_a ** 2 + num_b ** 2
  elif num_a > num_c and num_a > num_b:
    is_rectangular = num_a ** 2 == num_c ** 2 + num_b ** 2
  else:
    is_rectangular = num_b ** 2 == num_a ** 2 + num_c ** 2

print(f"Trojúhelník je {tringle_type}{', pravouhly' if is_rectangular else ''}")
