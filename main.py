# Currency Analysis
# Study change of currencies with addition to the database
from selenium import webdriver
from selenium.webdriver.common.by import By
import database
import os
import datetime
import configparser
from time import sleep
from pathlib import Path


def main(website: str):
    browser = webdriver.Firefox()
    browser.get(website)
    sleep(20)

    if not os.path.isfile('database.db'):
        new_files(browser)
        print('The database has been created')
        return

    config = configparser.ConfigParser()
    config.read('time.ini')

    current_date_website = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[4]/div[2]').text.split()[3]
    today = datetime.date.today()
    update_ini = datetime.datetime.strptime(config['DEFAULT']['update'], '%Y-%m-%d').date()

    if today == datetime.datetime.strptime(current_date_website, '%d.%m.%Y').date() and today != update_ini:
        data_list = []

        element = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/div')
        data = element.text.split('\n').__iter__()
        data.__next__().split()
        for _ in data:
            information = _.split()
            currency_name = ' '.join(information[3:-1])
            del information[3:-1]
            information.insert(3, currency_name)
            data_list.append(information)

        database.difference(tuple(data_list))
        database.updating_data(tuple(data_list))

        config = configparser.ConfigParser()
        my_file = Path('time.ini')
        config.read(my_file)
        config.set('DEFAULT', 'update', str(datetime.date.today()))
        config.write(my_file.open('w'))
        print('Data updated')
        return
    elif today == update_ini:
        print('The data was updated today')
        return
    else:
        print('There is no new data')
        return


def new_files(browser):
    database.new_base()
    new_data_list = []

    datum_point = str(datetime.date.today())
    current_date_website = browser.find_element(By.XPATH,
                                                '//*[@id="content"]/div/div/div/div[4]/div[2]').text.split()[3]
    last_update = str(datetime.datetime.strptime(current_date_website, '%d.%m.%Y').date())
    print(f'Starting point: {datum_point}')

    config = configparser.ConfigParser()
    config['DEFAULT']['starting_point'] = datum_point
    config['DEFAULT']['update'] = last_update
    with open('time.ini', 'w') as file:
        config.write(file)

    element = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/div')
    data = element.text.split('\n').__iter__()
    data.__next__().split()
    for _ in data:
        information = _.split()
        currency_name = ' '.join(information[3:-1])
        del information[3:-1]
        information.insert(3, currency_name)
        new_data_list.append(information)
    database.new_data(tuple(new_data_list))


if __name__ == '__main__':
    main('https://cbr.ru/curreNcy_base/daily/')
