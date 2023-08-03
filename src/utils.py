import string
from re import sub
import time

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def wait_for_player(player_name, driver, max_wait = 21):
    for i in range(1, max_wait):
        time.sleep(1)
        name = driver.find_element(By.CLASS_NAME, 'pp-player_name').text
        if name == player_name:
            return True
    raise Exception(f"Unable to load page for {player_name}")

def player_table_empty(player_table):
    try:
        player_table.find_element(By.CLASS_NAME, 'dataTables_empty')
        return True
    except NoSuchElementException:
        return False
    False

def correct_case(text):
    text = text.lower()
    text = text.split(sep=' ')
    text = [string.capwords(s) for s in text]
    text = ' '.join(text)
    text = text.split(sep='-')
    text = [string.capwords(s) for s in text]
    text = '-'.join(text)
    return text

def team_from_logo(src):
    logo = src.split('/')[-1]
    return logo.split('.')[0]

def snake_case(s):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()
