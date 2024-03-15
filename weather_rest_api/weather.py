from request_file import WeatherApp

weather = WeatherApp()

while True:
    print('1. Show weather data.')
    print('2. Add weather data.')
    print('3. Update weather data.')
    print('4. Delete weather data.')
    print('5. Exit')

    user_choice = int(input('Choose option: '))

    if user_choice == 1:
        print(weather.get())
    if user_choice == 2:
        location = str(input('Provide weather location: '))
        print(weather.post(location))
    if user_choice == 3:
        print(weather.patch())
    if user_choice == 4:
        location = str(input('Provide location you want to delete: '))
        print(weather.delete(location))
    if user_choice == 5:
        exit()
