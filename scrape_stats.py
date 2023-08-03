import time
from src.utils import correct_case, team_from_logo, snake_case, wait_for_player, player_table_empty

import numpy as np
import pandas as pd

from selenium import webdriver 
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
 
# the target website 
url = "https://footystatistics.com/index.php" 
 
# the interface for turning on headless mode 

options = Options() 
options.add_argument("--headless") 

# using Firefox headless webdriver to secure connection to Firefox 
with webdriver.Firefox(options=options) as driver: 
	# opening the target website in the browser 
	driver.get(url) 

	teams = driver.find_element(By.ID, 'teams_dropdown')
	team_list = [correct_case(team.text) for team in teams.find_elements(By.TAG_NAME, 'option')]
	teams_dropdown = Select(teams)

	for t in range(12, len(team_list)):
		team = team_list[t]
		print("--------------------------------")
		print(team)
		teams_dropdown.select_by_index(t)
		time.sleep(2)
		players = driver.find_element(By.ID, 'players_dropdown')
		player_list = [correct_case(player.text) for player in players.find_elements(By.TAG_NAME, 'option')]
		#print(player_list)
		players_dropdown = Select(players)

		for p in range(1, len(player_list)):
			try:
				players_dropdown.select_by_index(p)
				wait_for_player(player_list[p], driver)
				#print("-----------------------------")
				#print(player_list[p])

				player_stats = driver.find_element(By.ID, 'player-stats')
				player_name = player_stats.find_element(By.CLASS_NAME, 'pp-player_name').text
				player_table = player_stats.find_element(By.ID, 'player_match_stats_2018')
				#print("table found")

				if player_table_empty(player_table):
					raise NoSuchElementException

				stats = pd.read_html(player_table.get_attribute('outerHTML'))[0]
				stats.drop(stats.tail(1).index,inplace=True) # last row is averages
				#print("table extracted")

				squad_logos = player_table.find_elements(By.ID, 'squad_logo')
				logos = [team_from_logo(logo.get_attribute('src')) for logo in squad_logos]
				# print("logos extracted")
				# print("logo length:", len(logos))
				# print("dims data:", stats.shape)
				stats = stats.head(len(logos))

				stats.rename(columns={'Unnamed: 0': 'TEAM'}, inplace=True)
				stats['TEAM'] = logos
				stats['PLAYER'] = player_name
				#print("table modified")

				out_file = f"data/player_stats/{snake_case(player_name)}.csv"
				stats.to_csv(out_file, index=False)
				print(player_name, ": success")
				with open('data/player_scrape_outcome.csv', 'a') as ps:
					ps.write(f'"{player_name}","{team}",{stats.shape[0]},"success"\n')

			except NoSuchElementException:
				print(player_name, "no table data")
				with open('data/player_scrape_outcome.csv', 'a') as ps:
					ps.write(f'"{player_name}","{team}",0,"no data"\n')

			except:
				print(player_name, ": fail")
				with open('data/player_scrape_outcome.csv', 'a') as ps:
					ps.write(f'"{player_name}","{team}",0,"fail"\n')

	driver.quit()
