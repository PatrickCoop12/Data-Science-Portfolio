from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

url = r'https://www.nba.com/stats/teams/traditional'
driver = webdriver.Chrome()
driver.get(url)

sleep(10)

src = driver.page_source
parser = BeautifulSoup(src, 'lxml')
table = parser.find("div", attrs = {'class':'Crom_container__C45Ti crom-container'})
headers = table.findAll('th')
headerlist = [h.text.strip() for h in headers[0:]]
headerlist = [i for i in headerlist if 'RANK' not in i]
rows = table.findAll('tr')[1:]
stats =  [[td.text.strip() for td in rows[i].findAll('td')[0:]] for i in range(len(rows))]
nba_stats = pd.DataFrame(stats, columns = headerlist)

sleep(10)

button = driver.find_element(By.XPATH, r'/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/nav/div[3]/button')
button.click()
i = 2

driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/nav/div[3]/ul/li[{i}]').click()

sleep(10)

src = driver.page_source
parser = BeautifulSoup(src, 'lxml')
table = parser.find("div", attrs = {'class':'Crom_container__C45Ti crom-container'})
headers = table.findAll('th')
headerlist = [h.text.strip() for h in headers[0:]]
headerlist = [i for i in headerlist if 'RANK' not in i]
rows = table.findAll('tr')[1:]
stats =  [[td.text.strip() for td in rows[i].findAll('td')[0:]] for i in range(len(rows))]
nba_stats_adv = pd.DataFrame(stats, columns = headerlist)

sleep(10)

button = driver.find_element(By.XPATH, r'/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/nav/div[3]/button')
button.click()
i = 3

driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/nav/div[3]/ul/li[{i}]').click()

sleep(10)

src = driver.page_source
parser = BeautifulSoup(src, 'lxml')
table = parser.find("div", attrs = {'class':'Crom_container__C45Ti crom-container'})
headers = table.findAll('th')
headerlist = [h.text.strip() for h in headers[0:]]
headerlist = [i for i in headerlist if 'RANK' not in i]
rows = table.findAll('tr')[1:]
stats =  [[td.text.strip() for td in rows[i].findAll('td')[0:]] for i in range(len(rows))]
nba_stats_ff = pd.DataFrame(stats, columns = headerlist)

sleep(10)

button = driver.find_element(By.XPATH, r'/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/nav/div[3]/button')
button.click()
i = 4

driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/nav/div[3]/ul/li[{i}]').click()

sleep(10)

src = driver.page_source
parser = BeautifulSoup(src, 'lxml')
table = parser.find("div", attrs = {'class':'Crom_container__C45Ti crom-container'})
headers = table.findAll('th')
headerlist = [h.text.strip() for h in headers[0:]]
headerlist = [i for i in headerlist if 'RANK' not in i]
rows = table.findAll('tr')[1:]
stats =  [[td.text.strip() for td in rows[i].findAll('td')[0:]] for i in range(len(rows))]
nba_stats_misc = pd.DataFrame(stats, columns = headerlist)

sleep(10)

button = driver.find_element(By.XPATH, r'/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/nav/div[3]/button')
button.click()
i = 5

driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[3]/section[1]/div/nav/div[3]/ul/li[{i}]').click()

sleep(10)

src = driver.page_source
parser = BeautifulSoup(src, 'lxml')
table = parser.find("div", attrs = {'class':'Crom_container__C45Ti crom-container'})
headers = table.findAll('th')
headerlist = [h.text.strip() for h in headers[0:]]
headerlist = [i for i in headerlist if 'RANK' not in i]
rows = table.findAll('tr')[1:]
stats =  [[td.text.strip() for td in rows[i].findAll('td')[0:]] for i in range(len(rows))]
nba_stats_scor = pd.DataFrame(stats, columns = headerlist)

driver.close()

test = nba_stats.merge(nba_stats_adv, left_on=['Team'], right_on= ['TEAM'])

test2 = pd.merge(nba_stats,nba_stats_adv[['OffRtg', 'DefRtg', 'NetRtg', 'AST%',
        'AST/TO', 'ASTRatio', 'OREB%', 'DREB%', 'REB%', 'TOV%', 'eFG%', 'TS%',
        'PACE', 'PIE']],left_index=True, right_index=True, how='left')
#%%
test3 = pd.merge(test2,nba_stats_ff[['FTARate',]],left_index=True, right_index=True, how='left')

test4 = pd.merge(test3,nba_stats_misc[['PTSOFF TO', '2ndPTS', 'FBPs',
        'PITP']], left_index=True, right_index=True, how='left')

test5 = pd.merge(test4,nba_stats_scor[['%FGA2PT', '%FGA3PT', '%PTS2PT',
        '%PTS2PT- MR', '%PTS3PT', '%PTSFBPs', '%PTSFT', '%PTSOffTO', '%PTSPITP',
        '2FGM%AST', '2FGM%UAST', '3FGM%AST', '3FGM%UAST', 'FGM%AST',
        'FGM%UAST']], left_index=True, right_index=True, how='left')


test6 = test5.drop(columns=['','BLKA','PFD','+/-'])

test6.to_excel('nba_current_stats1.xlsx', index= False)

test87 = pd.concat([test6.loc[test6['Team'] == 'Milwaukee Bucks'].iloc[:,6:].reset_index(), test6.loc[test6['Team'] == 'Dallas Mavericks'].iloc[:,6:].reset_index()], axis= 1)

test87.drop(columns=['index'])