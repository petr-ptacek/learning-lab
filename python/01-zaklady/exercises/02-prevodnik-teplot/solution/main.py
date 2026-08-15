value_to_conversion = float(input("Zadej hodnotu: "))
value_unit = input("Zadej jednotku (C, F, K): ")

value_fahrenheit = 0
value_celsius = 0
value_kelvin = 0

if value_unit == "C":
  value_celsius = value_to_conversion
  value_fahrenheit = ((value_celsius * 9) / 5) + 32
  value_kelvin = value_celsius + 273.15
elif value_unit == "F":
  value_fahrenheit = value_to_conversion
  value_celsius = (value_fahrenheit - 32) * 5 / 9
  value_kelvin = (value_fahrenheit - 32) * 5 / 9 + 273.15
else:
  value_kelvin = value_to_conversion
  value_celsius = value_kelvin - 273.15
  value_fahrenheit = ((value_kelvin - 273.15) * 9 / 5) + 32

result = "Celsius:\t{c} °C\nFahrenheit:\t{f} °F\nKelvin:\t\t{k} K".format(
    c=round(value_celsius, 1),
    f=round(value_fahrenheit, 1),
    k=round(value_kelvin, 1)
)

print(result)
