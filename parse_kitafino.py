from bs4 import BeautifulSoup
import datetime

def extract_meal_data(html_content):

    meals = []

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'lxml')

    # Find all order sections for meals
    meal_items = soup.find_all('div', class_='order_table')

    # Iterate through the found elements and extract information
    for item in meal_items:
        # Find the day of the week
        day_of_week = item.find('strong').text.strip()
        meal_date = datetime.datetime.strptime(day_of_week.split()[1], '%d.%m.%Y').date()

        dish_name = item.find('span', class_='preis_info_zu_men')
        if not dish_name:
            meals.append( (meal_date, None) )
            continue

        dish_name = dish_name.next_sibling.strip()
        price = item.find('div', class_='preis_button').text.strip()

        #print(f'{meal_date}: {dish_name} - Price: {price}')
        meals.append( (meal_date, dish_name) )

    return meals

if __name__ == "__main__":
    # Load HTML content from a .txt file
    with open('kitafino_raw.txt', 'r') as file:
        html_content = file.read()

    # Call the function to extract meal data
    meals = extract_meal_data(html_content)
    print(meals)