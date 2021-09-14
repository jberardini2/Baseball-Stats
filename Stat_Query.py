#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Selenium Getting data from MLB/standings
from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
datetime_local = datetime.now()

# The variable division needs to be set to the one to review.
# American League West = regularSeason-division-200
# American League East = regularSeason-division-201
# American League Central = regularSeason-division-202
# National League West = regularSeason-division-203 
# National League East = regularSeason-division-204
# National League Central = regularSeason-division-205
# Selenium global driver 
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.mlb.com/standings")

class Stat_Query:
    def __init__(self, d="regularSeason-division-203"):
        self.division = d
        self.current_records_dict = {}
        self.URL_List = []
        self.gameDates = []
            
    # ************************  Get Full Team Name and Current Record from the Standings ***************************
    def getCurrentRecords(self):

        try: # This is used to wait for the web page to load before executing anything.
            teamAndCurrentRecord = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "main")))
            
            firstTeamName  = teamAndCurrentRecord.find_element_by_xpath("//*[@id='" + self.division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/a")
            firstWins      = teamAndCurrentRecord.find_element_by_xpath("//*[@id='" + self.division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[2]/span")
            firstLosses    = teamAndCurrentRecord.find_element_by_xpath("//*[@id='" + self.division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[3]/span")

            secondTeamName = teamAndCurrentRecord.find_element_by_xpath("//*[@id='" + self.division + "']//div//div//div[1]//div//table/tbody//tr[2]//td[1]/span/span/a")
            secondWins     = teamAndCurrentRecord.find_element_by_xpath("//*[@id='" + self.division + "']//div//div//div[1]//div//table/tbody//tr[2]//td[2]/span")
            secondLosses   = teamAndCurrentRecord.find_element_by_xpath("//*[@id='" + self.division + "']//div//div//div[1]//div//table/tbody//tr[2]//td[3]/span")
            
            current_records_dict = {firstTeamName.get_attribute("data-team-name"):
                                            {firstWins.text: firstLosses.text}, 
                                            secondTeamName.get_attribute("data-team-name"):
                                            {secondWins.text: secondLosses.text}
                                     }
                   
            # if I make current_records_dict private "_current_records_dict", it won't return
            # a dictionary that is needed for reporting. 
            return current_records_dict
                      
        finally:
            pass
            
    # ************************  Create the URL for the teams schedule **********************************************
    def getScheduleURL(self):    
        self.URL_List = []
        
        try: 
            teamNameForScheduleURL = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='" + self.division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/span/span/a")))
            # do from outside: wt_href = teamNameForScheduleURL.get_attribute("href")  # winning team url link for reporting
            # move to next class gamesOver500,  w_opponent_win_loss_list_of_dict, w_opponent_team_dict = get_opponent_info(teamNameForScheduleURL)            
            self.URL_List.append(teamNameForScheduleURL.get_attribute("href"))
                    
        finally:
            pass
        
        # Get the trailing team's schedule URL:
        try: 
            teamNameForScheduleURL = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[@id='" + self.division + "']//div//div//div[1]//div//table/tbody//tr[2]//td[1]/span/span/span/span/a")))
            # do from outside: tt_href = teamNameForScheduleURL.get_attribute("href")  # trailing team url link for reporting
            # move to next class gamesOver500,  t_opponent_win_loss_list_of_dict, t_opponent_team_dict = get_opponent_info(teamNameForScheduleURL)            
            self.URL_List.append(teamNameForScheduleURL.get_attribute("href"))

        finally:
            pass
                
        return self.URL_List
    
    # ************************ Get List of Games Dates ************************************************************
    def getScheduleDates(self, U):    
        self.URL_ForSchedule = U
     
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        
        # Open full schedule page. Substitute team name and year in URL: https://www.mlb.com/giants/schedule/2021/fullseason      
        driver.get(self.URL_ForSchedule + "/schedule/" + datetime_local.strftime('%Y') + "/fullseason" )
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        # format and get today's date and find match against schedule's dates stored in list.
        dayStripped = datetime_local.strftime('%d').lstrip("0")
        month = datetime_local.strftime('%b')
        todaysDate = month + " " + dayStripped
    
        try: # Get all the dates for games played for the season and put in list.
            main = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='month-date']")))
        
            time.sleep(10) 
           
            monthdate = main.find_elements_by_xpath("//div[@class='month-date']")

            self.gameDates = []
            
            for date in monthdate:
                self.gameDates.append(date.text)
            
            # Clean up gameDates and remove blank entries. 
            for index, goodDate in enumerate(self.gameDates):
                if not goodDate:
                    del self.gameDates[index]
                    
            return self.gameDates
        
        finally:
            pass 

        
        
    # ************************ Get Team Played and how many remaining games **************************  
    def getTeamNameAndCountOfGamesRemaining(self, U, G):
        self.URL_Schedule = U
        self.gameDates = G
    
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)

        # Open full schedule page. Substitute team name and year in URL: https://www.mlb.com/giants/schedule/2021/fullseason      
        driver.get(self.URL_Schedule + "/schedule/" + datetime_local.strftime('%Y') + "/fullseason" )
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
   
        # format and get today's date and find match against schedule's dates stored in list.
        dayStripped = datetime_local.strftime('%d').lstrip("0")
        month = datetime_local.strftime('%b')
        todaysDate = month + " " + dayStripped
        
        # This will find the latest date where a game is played. It's need to find tomorrow's game when there's a day off.
        for index, date in enumerate(self.gameDates):
            if datetime.strptime(date, "%b %d") >= datetime.strptime(todaysDate, "%b %d"):
                indexLocation = index # save the index location so I know where to select start grabbing
                # exit out of for loop after finding first good date.
                break
 
        opponent_team_dict = {}
    
        # iterate through the rest of the schedule, look up team played and count how many
        for index, date in enumerate(self.gameDates):
            if index >= indexLocation: # Start processing on today's date until end of season.

                try: 
        
                    main = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.XPATH, "//div[text()='" + date + "']//ancestor::tr//td[2]//div/div[5][@class='opponent-tricode']")))
            
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
                    tricode = main.get_attribute('innerHTML')
                    if tricode in opponent_team_dict:
                        opponent_team_dict[tricode] += 1
                    else: # Add team to dictionary and start at 1 game played.
                        opponent_team_dict[tricode] = 1
    
                finally:
                    pass
    
        return opponent_team_dict
    
    # ************************ Get Win/Loss Records for Opponents ************************** 
    def getWinLossRecordForOpponent(self, O):
        self.Opponent_Team_Dict = O
  
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        driver.get("https://www.mlb.com/standings")
        
        opponent_win_loss_list_of_dict = []
   
        for key, value in self.Opponent_Team_Dict.items():
            #  After finding team tricode (LAD, CIN, SF) The ancestor travels from the child span all the way up to tr. 
            try: 
                wins = WebDriverWait(driver,  20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[text()='" + key + "']//ancestor::tr//td[2]//span")))                    
            
            finally:
                pass
 
            try:
                losses = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//a[text()='" + key + "']//ancestor::tr//td[3]//span")))                    
         
            finally:
                pass
        
            # Creating current opponent wins and losses
            opponent_wins_loss_dict = {key: {wins.text: losses.text}}
            opponent_win_loss_list_of_dict.append(opponent_wins_loss_dict)
        
        return opponent_win_loss_list_of_dict

