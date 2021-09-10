#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
import time

# Selenium global driver 
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.mlb.com/standings")

# The variable division needs to be set to the one to review.
# American League West = regularSeason-division-200
# American League East = regularSeason-division-201
# American League Central = regularSeason-division-202
# National League West = regularSeason-division-203 
# National League East = regularSeason-division-204
# National League Central = regularSeason-division-205
      
division = "regularSeason-division-203" # NL West

from datetime import datetime
datetime_local = datetime.now()
date_display = datetime_local.strftime('%A - %B %d, %Y')
print ("\t" + date_display)

# Used for reporting. Team names and href:
g_winning_team_name = ''
g_trail_team_name = ''
g_wt_href = ''
g_tt_href = ''

tup_win_perc = (.200,.250,.300,.350,.400,.450,.500,.550,.600,.650,.700,.750)

def retrieve_record():
    
    current_records_dict = {}
    
    try: # This is used to wait for the web page to load before executing anything.
        main = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        )
       
        firstTeamName  = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/a")
        firstWins      = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[2]/span")
        firstLosses    = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[3]/span")

        secondTeamName = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[2]//td[1]/span/span/a")
        secondWins     = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[2]//td[2]/span")
        secondLosses   = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[2]//td[3]/span")

        current_records_dict = {firstTeamName.get_attribute("data-team-name"):
                                    {firstWins.text: firstLosses.text}, 
                                secondTeamName.get_attribute("data-team-name"):
                                    {secondWins.text: secondLosses.text}
                               }
          
        return current_records_dict
              
    finally:
        pass
          
    
def games_remaining(wins, losses):
    
    games_played = wins + losses
    games_remain = 162 - games_played
    
    return games_remain


def calc_win_perc(winning_list_of_dict,team_name, wins, losses):
    
    games_remain = games_remaining(wins, losses)
    
    dict_team_results = {}
   
    for perc in tup_win_perc:
        calc_wins = perc * games_remain
        calc_losses = games_remain - calc_wins
        final_wins = wins + calc_wins 
        final_losses = losses + calc_losses
       
        final_record = "Final_Record"
        dict_team_results = {team_name: 
                             {str(round(calc_wins )): str(round(calc_losses ))}, 
                             final_record:  
                             {str(round(final_wins)): str(round(final_losses))}
                            }
        winning_list_of_dict.append(dict_team_results)
    return winning_list_of_dict

def trailing_team(win_list_of_dict, team_name, wins, losses):
    
    dict_trail_team_results = {}
    trailing_list_of_dict = []
    for win_dict in win_list_of_dict:
        for key, value in win_dict.items():
            #print(key + "**") # "Giants" and "Final Record"
            if isinstance(value, dict):
                for winlossrec in value.items():
                    if key == "Final_Record":
                        #print (winlossrec)
                       
                        trail_wins = int(winlossrec[0]) - wins
                        trail_losses = int(winlossrec[1]) - losses
                        trail_final_wins = wins + trail_wins
                        trail_final_losses = losses + trail_losses
                       # print (str(trail_wins) + "-" + str(trail_losses))
                       # print (str(trail_final_wins) + "-" + str(trail_final_losses))
                        
                        final_record = "Final_Record"
                        dict_trail_team_results = {team_name: 
                                                     {str(round(trail_wins )): str(round(trail_losses ))}, 
                                                    final_record:  
                                                     {str(round(trail_final_wins)): str(round(trail_final_losses))}
                                                    }
                        trailing_list_of_dict.append(dict_trail_team_results)
   
       
    return  trailing_list_of_dict

def over_under_calc_tally(opponent_win_loss_list_of_dict, opponent_team_dict):
    
    #print (opponent_win_loss_list_of_dict)
    #print (opponent_team_dict)
    gamesOver500 = 0
    for dict_record in opponent_win_loss_list_of_dict:
        for key,value in dict_record.items():
            # print (key)
            for wl in value.items():
                #print (wl[0])
                #print (wl[1])
                over500 = int(wl[0]) - int(wl[1])
                
                if over500 > 0:
                    if key in opponent_team_dict.keys():
                        #print (opponent_team_dict[key])
                        gamesOver500 = gamesOver500 + int(opponent_team_dict[key])
    
    return(gamesOver500)
                

# ######################################################
def get_opponent_info(teamInfoURL):

    PATH="C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
            
    # Open full schedule page. Substitute team name and year in URL: https://www.mlb.com/giants/schedule/2021/fullseason      
    driver.get(teamInfoURL.get_attribute("href") + "/schedule/" + datetime_local.strftime('%Y') + "/fullseason" )
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    gameDates = []
        
    # format and get today's date and find match against schedule's dates stored in list.
    dayStripped = datetime_local.strftime('%d').lstrip("0")
    month = datetime_local.strftime('%b')
    todaysDate = month + " " + dayStripped
    
    try: # Get all the dates for games played for the season and put in list.
        main = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='month-date']")))
        
        time.sleep(10) 
        monthdate = main.find_elements_by_xpath("//div[@class='month-date']")
        for date in monthdate:
            gameDates.append(date.text)
        
        # Clean up gameDates and remove blank entries. xxx
        for index, goodDate in enumerate(gameDates):
            if not goodDate:
                del gameDates[index]
        
    finally:
        pass    
    
    #print (gameDates)
    
    # This will find the latest date where a game is played. It's need to find tomorrow's game when there's a day off.
    for index, date in enumerate(gameDates):
        if datetime.strptime(date, "%b %d") >= datetime.strptime(todaysDate, "%b %d"):
            indexLocation = index # save the index location so I know where to select start grabbing
            # exit out of for loop after finding first good date.
            break
                                  # teams 
    #print (gameDates)        
    # print ("indexLocation: " + str(indexLocation))
        
    opponent_team_dict = {}
    
    # iterate through the rest of the schedule, look up team played and count how many
    for index, date in enumerate(gameDates):
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
   
   # print ("Opponent_team_dict:")
   # print (opponent_team_dict)
    
    # Selenium global driver 
  
    PATH="C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.mlb.com/standings")
    
    opponent_win_loss_list_of_dict = []
   
    for key, value in opponent_team_dict.items():
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
            
 
    #print (opponent_win_loss_list_of_dict)
    gamesOver500 = over_under_calc_tally(opponent_win_loss_list_of_dict,opponent_team_dict)
    return (gamesOver500,  opponent_win_loss_list_of_dict, opponent_team_dict)
    
def over_under_calc():
   
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.mlb.com/standings")
    
    # Get the 1st place team's schedule URL:
    try: 
        teamNameForScheduleURL = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/span/span/a")))
        g_wt_href = teamNameForScheduleURL.get_attribute("href")  # winning team url link for reporting
        w_gamesOver500,  w_opponent_win_loss_list_of_dict, w_opponent_team_dict = get_opponent_info(teamNameForScheduleURL)            

    finally:
        pass
        
    # Get the trailing team's schedule URL:
    try: 
        teamNameForScheduleURL = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[2]//td[1]/span/span/span/span/a")))
        g_tt_href = teamNameForScheduleURL.get_attribute("href")  # trailing team url link for reporting
        t_gamesOver500,  t_opponent_win_loss_list_of_dict, t_opponent_team_dict = get_opponent_info(teamNameForScheduleURL)            

    finally:
        pass
                
        # print team name, href, over 500 total and opponents with number of games left.
        print ("\t     ", g_winning_team_name)
        print ("\t     ", g_wt_href)
        print ("Total number of games left against over 500 teams is " + str(w_gamesOver500) + ".")
        print ("Opponents and number of games left:")
        print (w_opponent_team_dict)
        print ()
        print ()
        print ("\t     ", g_trail_team_name)
        print ("\t     ", g_tt_href)
        print ("Total number of games left against over 500 teams is " + str(t_gamesOver500) + ".")
        print ("Opponents and number of games left:")
        print (t_opponent_team_dict)
        
        #print (w_opponent_win_loss_list_of_dict)  # has win loss record of opponents. 
        #print (t_opponent_win_loss_list_of_dict)
        
        return ()
    
# *********** calc_winning_percentage ***************
def calc_winning_percentage(wins,losses):
    total = float(wins) + float(losses)
    win_percentage = float(wins)/float(total)
    return win_percentage

def format_win_perc(win_perc):
    
    wp = str(win_perc)
    wp = wp[1:5]
    wp = wp.ljust(4, '0')
    return wp
                    
# ************ print_team_results **************
def print_team_results(win_list, trail_list):
      
    print()
    print()
    print ("\t     ", "Projected Record and",  "\t\t", "Final Record and")
    print ("\t     ", "Winning Percentage","\t\t", "Winning Percentage")
    counter = 0
    for win_dict in win_list:
        print ()
        counter = counter + 1
        counter_format = str(counter).ljust(2, ' ')
        space3 = '   '
        for key, value in win_dict.items():
            if key == "Final_Record":
                print(space3,counter_format,space3, end='') # Skip "Final_Record"
            else:
                print(space3, counter_format,space3, key,end='') # key = "Giants"
                
            if isinstance(value, dict):
                for winlossrec in value.items():
                    win_perc = calc_winning_percentage(float(winlossrec[0]),float(winlossrec[1]))
                    wp = format_win_perc(win_perc)
                   # print (winlossrec,"{:.3f}".format(win_perc), "\t", end='')
                    #print (winlossrec, wp, "\t", end='')
                    print ("  ",winlossrec[0],"-",winlossrec[1], wp, "\t\t", end='')
                    
    print ()
    print ()
    counter = 0
    for trail_dict in trail_list:
        print ()
        counter = counter + 1
        counter_format = str(counter).ljust(2, ' ')
        for key, value in trail_dict.items():
            if key == "Final_Record":
                print(space3, counter_format,"  ", end='') # Skip "Final Record"
            else:
                print(space3, counter_format,"  ", key,end='') # key = "Dodgers"
            
            if isinstance(value, dict):
                for winlossrec in value.items():
                    win_perc = calc_winning_percentage(float(winlossrec[0]),float(winlossrec[1]))
                    wp = format_win_perc(win_perc)
                    #print (winlossrec,"{:.3f}".format(win_perc), "\t", end='')
                    #print (winlossrec, wp, "\t", end='')
                    print ("  ", winlossrec[0],"-",winlossrec[1], wp, "\t\t", end='')                       

# ***********************************************************************************************

list_of_dict = []
trail_list_of_dict = []


# w = winning and t = trailing

todays_team_record_dict = retrieve_record()

place = 1
for key, value in todays_team_record_dict.items():
    #print("key: " + key) # 1st and 2nd place team name
    if place == 1:
        w_team = key
        g_winning_team_name = w_team # global for reporting
    else:
        t_team = key
        g_trail_team_name = t_team # global for reporting
    for winlossrec in value.items():
        if place == 1:
            w_team_wins = int(winlossrec[0])
            w_team_losses = int(winlossrec[1])
        else: 
            t_team_wins = int(winlossrec[0])
            t_team_losses = int(winlossrec[1])
    place += 1

winning_list_of_dict = calc_win_perc(list_of_dict,w_team,w_team_wins,w_team_losses)
trail_list_of_dict = trailing_team(winning_list_of_dict,t_team,t_team_wins,t_team_losses)

print ()
games_remain_w_team = games_remaining(w_team_wins,w_team_losses)
games_remain_t_team = games_remaining(t_team_wins,t_team_losses)
games_back = ((w_team_wins - t_team_wins) + (t_team_losses - w_team_losses)) / 2
print ("Current Records:", "\t\t\t\t", "Games Remaining")
print ( w_team,"\t\t", w_team_wins,"-", w_team_losses,"\t\t\t", games_remain_w_team  )
print ( t_team,"\t\t", t_team_wins,"-", t_team_losses, "  ", str(games_back) + "gb" ,"\t\t",str(games_remain_t_team)  )

report_results = print_team_results(winning_list_of_dict, trail_list_of_dict)

print ()
print ()
magic_number = (162 + 1 ) - (w_team_wins + t_team_losses)
print ("The", w_team,"magic number to clinch the division is ", str(magic_number))
print ()
print ()
over_under_calc()
print ()
print ()
print ("The winning team percentages are calculated and rounded from the following: ")
print (tup_win_perc)

driver.quit()
print ()
print ("\t\t\t\t", "end of report")


# In[25]:


opponent_team_dict = {'CHC': 3, 'SD': 10, 'ATL': 3, 'COL': 3, 'ARI': 3} 
key = 'ARI'
if key in opponent_team_dict.keys():
    print (opponent_team_dict[key])
    #gamesOver500 = gamesOver500 + int(opponent_team_dict[key])


# In[3]:


# Clean up gameDates and remove blank entries.
gameDates = ['Apr 1', 'Apr 2', 'Apr 3', 'Apr 5', 'Apr 6', 'Apr 7', 'Apr 9', 'Apr 10', 'Apr 11', 'Apr 12', 'Apr 13', 'Apr 14', 'Apr 16', 'Apr 17', 'Apr 18', 'Apr 19', 'Apr 20', 'Apr 21', 'Apr 22', 'Apr 23', 'Apr 24', 'Apr 25', 'Apr 26', 'Apr 27', 'Apr 28', 'Apr 30', 'May 1', 'May 2', 'May 3', 'May 4', '', 'May 5', 'May 7', 'May 8', 'May 9', 'May 10', 'May 11', 'May 13', 'May 14', 'May 15', 'May 16', 'May 17', 'May 18', 'May 19', 'May 20', 'May 21', 'May 22', 'May 23', 'May 25', 'May 26', 'May 27', 'May 28', 'May 29', 'May 30', 'May 31', 'Jun 1', 'Jun 3', 'Jun 4', 'Jun 5', 'Jun 6', 'Jun 8', 'Jun 9', 'Jun 10', 'Jun 11', 'Jun 12', '', 'Jun 13', 'Jun 14', 'Jun 15', 'Jun 16', 'Jun 17', 'Jun 18', 'Jun 19', 'Jun 20', 'Jun 22', 'Jun 23', 'Jun 25', 'Jun 26', 'Jun 27', 'Jun 28', 'Jun 29', 'Jul 1', 'Jul 2', 'Jul 3', 'Jul 4', 'Jul 5', 'Jul 6', 'Jul 7', 'Jul 9', 'Jul 10', 'Jul 11', 'Jul 16', 'Jul 17', 'Jul 18', 'Jul 19', 'Jul 20', 'Jul 21', 'Jul 22', 'Jul 23', 'Jul 24', 'Jul 25', 'Jul 27', 'Jul 28', 'Jul 29', 'Jul 30', 'Jul 31', 'Aug 1', 'Aug 2', 'Aug 3', 'Aug 4', 'Aug 5', 'Aug 6', 'Aug 7', 'Aug 8', 'Aug 10', 'Aug 11', 'Aug 12', 'Aug 13', 'Aug 14', 'Aug 15', 'Aug 16', 'Aug 17', 'Aug 18', 'Aug 20', 'Aug 21', 'Aug 22', 'Aug 24', 'Aug 25', 'Aug 26', 'Aug 27', 'Aug 28', 'Aug 29', 'Aug 30', 'Aug 31', 'Sep 1', 'Sep 2', 'Sep 3', 'Sep 4', 'Sep 5', 'Sep 6', 'Sep 7', 'Sep 8', 'Sep 10', 'Sep 11', 'Sep 12', 'Sep 13', 'Sep 14', 'Sep 15', 'Sep 16', 'Sep 17', 'Sep 18', 'Sep 19', 'Sep 21', 'Sep 22', 'Sep 23', 'Sep 24', 'Sep 25', 'Sep 26', 'Sep 28', 'Sep 29', 'Sep 30', 'Oct 1', 'Oct 2', 'Oct 3', '']
for index, goodDate in enumerate(gameDates):
   if not goodDate:
       del gameDates[index]
       
print (gameDates)
           

               


# In[28]:


import time
datetime_local = datetime.now()
date_display = datetime_local.strftime('%A - %B %d, %Y')
print ("\t" + date_display)
from datetime import datetime

gameDates = ['Sep 18', 'Sep 19', 'Sep 21', 'Sep 22', 'Sep 23', 'Sep 24', 'Sep 25', 'Sep 26', 'Sep 28', 'Sep 29', 'Sep 30', 'Oct 1', 'Oct 2', 'Oct 3']

# format and get today's date and find match against schedule's dates stored in list.
dayStripped = datetime_local.strftime('%d').lstrip("0")
month = datetime_local.strftime('%b')
todaysDate = month + " " + dayStripped
todaysDate = "Sep 24"

print ("Todays Date")
print (type(todaysDate))
print (todaysDate + " " + str(len(date)))
print ("****************")
d1 = datetime.strptime(todaysDate, "%b %d")
print (d1)

for index, date in enumerate(gameDates):
   # print (type(date))
   # print (date + " " + str(len(date)))
   # print (index)
    # convert string to date in format "Mmm d(dd) before >= comparison."
    if datetime.strptime(date, "%b %d") >= datetime.strptime(todaysDate, "%b %d"):
        indexLocation = index 
        print ("Date is >= Today's Date") 
        print (date + " >= " +  todaysDate)


# In[59]:


#   #linkPath.findElement("//a[@href]").click()
      #linkPath = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/span/span/a[contains(@href)]") fail
      #linkPath = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/span/span/a[contains(@href,'giants')]")  this works
      #linkPath = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/span/span/a") original from above 
      
      # stopped here trying to find first place team and click link
      # linkPath = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/span/span/a")
      # print (linkPath)
  
      #'//a[contains(@href,"href")]'
      # webDriver.findElement(By.xpath("//a[@href='/docs/configuration']")).click();
      
      #    link = driver.find_element_by_link_text("Python Programmdding")
      #    link.click()
      
      
      #secondTeamName = main.find_element_by_xpath("//*[@id='regularSeason-division-203']//div//div//div[1]//div//table/tbody//tr[2]//td[1]/span/span/a")

      #current_records_dict = {firstTeamName.get_attribute("data-team-name"):
      #                            {firstWins.text: firstLosses.text}, 
      #                        secondTeamName.get_attribute("data-team-name"):
      #                            {secondWins.text: secondLosses.text}
      ##                       }
      
      #    EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials")) # clicking a link
      #  )
      ##  element.clear() # clear the 
      # element.click()


# In[1]:


#!/usr/bin/env python
# coding: utf-8
# Selenium Getting data from MLB/standings
from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from datetime import datetime
datetime_local = datetime.now()


# Selenium global driver 
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.mlb.com/giants/schedule/2021/fullseason")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def over_under_calc():
   
    gameDates = []
    
    print ("hi")
    
    # format and get today's date and find match against schedule's dates stored in list.
    dayStripped = datetime_local.strftime('%d').lstrip("0")
    month = datetime_local.strftime('%b')
    todaysDate = month + " " + dayStripped
    
    try: # Get all the dates for games played for the season and put in list.
        main = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='month-date']")))
        
        time.sleep(10) 
        monthdate = main.find_elements_by_xpath("//div[@class='month-date']")
        for date in monthdate:
            gameDates.append(date.text)
        
        # The last record is always blank. Deleting it to help stop error processing below.
        del gameDates[-1]
        #print (gameDates)
                                                    
    finally:
        pass      
    
    for index, date in enumerate(gameDates):
        if date == todaysDate:
            indexLocation = index # save the index location so I know where to start grabbing
                                  # teams 
            
   # print ("indexLocation: " + str(indexLocation))
        
    team_dict = {}
    
    # iterate through the rest of the schedule, look up team played and count how many
    for index, date in enumerate(gameDates):
        if index >= indexLocation: # Start processing on today's date until end of season.
            try: 
                main = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//div[text()='" + date + "']//parent::td//parent::tr//td[2]//div/div[5][@class='opponent-tricode']")))
                if main.text in team_dict:
                    team_dict[main.text] += 1
                else: # Add team to dictionary and start at 1 game played.
                    team_dict[main.text] = 1
    
            finally:
                pass
            #except: # was getting an error on the last record of gameDates being blank.  
            #    pass
   
    driver.quit()

    print (team_dict)
    
    # next look up record in schedule page and tally for over or under 500 -
    for key, value in team_dict.items():
        print (key)
        print (value)
        
      
        # look up schedule for team and get wins and losses.
        # dictionary will be {teamname:wins|losses}
        # pass on to report and allow to calculate in report routine.  Gives flexibility.
    
        
        
        
        
       
    
    
        
      
    
over_under_calc()



# In[86]:


from datetime import datetime
datetime_local = datetime.now()
dayStripped = datetime_local.strftime('%d').lstrip("0")
month = datetime_local.strftime('%b')
print (month + " " + dayStripped)


# In[2]:


#!/usr/bin/env python
# coding: utf-8
# Selenium Getting data from MLB/standings
from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# Selenium global driver 
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
date = 'Apr 10'
driver.get("https://www.mlb.com/dodgers/schedule/2021/fullseason")

try: 
    #/html/body/main/div[2]/div/div/div/div/div[1]/div[5]/div[321]/table/tbody/tr[1]/td[2]/div[1]/div[5]
    main = WebDriverWait(driver, 30).until(
        #EC.presence_of_element_located((By.XPATH, "//div[text()='" + date + "']//ancestor::tr//td[2]//div/div[4]")))
        EC.presence_of_element_located((By.XPATH, "//div[text()='" + date + "']//ancestor::tr//td[2]//div/div[5][@class='opponent-tricode']")))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    (main.get_attribute('innerHTML'))
finally:
    pass


print (type(main))
print (main.text)
print (main.get_property('text'))
print (main.get_attribute('text'))
print (main.get_property('value'))
print (main.get_attribute('value'))
#THE FOLLOWING 2 WORKED FOR HTML THAT LOOKS LIKE THIS:
#<div class="opponent-tricode">MIA</div>
print (main.get_attribute("class"))
print (main.get_attribute('innerHTML'))  # THIS WORKS!!!!


#print (main.get_attribute('opponent-tricode'))
#print (main.get_property('opponent-tricode'))
  

#teamname4 = driver.find_element_by_xpath("//div[@class='month-date']//parent::td//parent::tr//td[2]//div/div[5][@class='opponent-tricode']")
print ("****!!****************")
#print (teamname4.text)        


# In[ ]:


# Get a list of dates (MMM D) of games
 #   try: # This is used to wait for the web page to load before executing anything.
 #       main = WebDriverWait(driver, 15).until(
 #           EC.presence_of_element_located((By.XPATH, "//div[@class='month-date']"))

       # for date in monthdate:
       #     gameDates.append(date.text)

#        monthdate = main.find_elements_by_xpath("//div[@class='month-date']")
#        for date in monthdate:
#            gameDates.append(date.text)

#        print (gameDates)

#        dayStripped = datetime_local.strftime('%d').lstrip("0")
#        month = datetime_local.strftime('%b')
#        todaysDate = month + " " + dayStripped

#        for date in gameDates:
#            if date == todaysDate:

   # print (dateLocate)         


# In[37]:


# List example!!!!!!!

gameDates = ["Apr 1", "Apr 2", "Apr 3"]

todaysDate = "Apr 2"
for date in gameDates:
    if date == todaysDate:
        exit
        
restOfScheduleIndex = gameDates.index(todaysDate)
#print (gameDates[restOfScheduleIndex])

for index, val in enumerate(gameDates):
    print (index, val)


print (index)



# In[ ]:


# format and get today's date and find match against schedule's dates stored in list.
dateToStrip = 'Apr '
str(dateToStrip[5:7])
dayStripped = datetime_local.strftime('%d').lstrip("0")
month = datetime_local.strftime('%b')
todaysDate = month + " " + dayStripped


# In[58]:



team = "Dbacks" # main.text
team_dict = {'Dodgers':3, 'Padres': 6, 'Dbacks': 1}
                

    #teamName = team_dict['Dodgers']; gets value
    #teamName = team_dict.get(team) gets value instead of key

if team in team_dict:
    team_dict[team] += 1
else:
    team_dict[team] = 1


print (team_dict)
        
"""
                                                  #   {str(round(trail_wins )): str(round(trail_losses ))}, 
                                                  #  final_record:  
                                                  #   {str(round(trail_final_wins)): str(round(trail_final_losses))}
                                                  #  }
               if main.text in team_dict:
                    team_dict[main.text] += 1
                else:
                    team_dict[main.text] = 1
               
                team_dict_list.append(team_dict)
"""         


# In[ ]:


# extra code not used    
    
        print (date)
        print (main.text)
        
        teamname = team_dict.get(main.text)
        if teamname
       
        team_dict = {main.text:} 
                                          #   {str(round(trail_wins )): str(round(trail_losses ))}, 
                                          #  final_record:  
                                          #   {str(round(trail_final_wins)): str(round(trail_final_losses))}
                                          #  }
                
    
        if main.text in team_dict:
            team_dict[main.text] += 1
        else:
            team_dict[main.text] = 1
        
        team_dict_list.append(team_dict)
    
        # For each date matched go get team played and count. Keep track in dictionary.
        #teamPlayed = main.find_element_by_xpath("//div[@class='month-date']//parent::td//parent::tr//td[2]//div/div[5][@class='opponent-tricode']")
        #print (teamPlayed.text)


# In[6]:


from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Selenium global driver 
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.mlb.com/standings")

opponent_win_loss_list_of_dict = []

#team_dict = {'MIL': '1', 'LAD': '3', 'COL': '6', 'CHC': '3', 'SD': '10', 'ATL': '3', 'ARI': '3'}
team_dict = {'COL': 4, 'CHC': 3, 'SD': 10, 'ATL': 3, 'ARI': 3}


for key, value in team_dict.items():
  #  print (key)
   # print (value)

    # After finding team tricode (LAD, CIN, SF) The ancestor travels from the child span all the way up to tr. 
    # Absolute path: /html/body/main/div[2]/div/div/div/section/section/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[2]/td[1]/span/span/span[1]/span[3]/a
    
    try: 
        wins = WebDriverWait(driver,  40).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='" + key + "']//ancestor::tr//td[2]//span")))                    
#        print (wins.text)
    finally:
        pass

    
    try:
        losses = WebDriverWait(driver,  40).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='" + key + "']//ancestor::tr//td[3]//span")))                    
    finally:
        pass
    
    # Creating current opponent wins and losses
    opponent_wins_loss_dict = {key: {wins.text: losses.text}}
    opponent_win_loss_list_of_dict.append(opponent_wins_loss_dict)
    
driver.quit()
        

print (opponent_win_loss_list_of_dict)
    
# print (main.get_attribute("class"))
# print (main.get_property('text')) 
# /html/body/main/div[2]/div/div/div/section/section/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[2]/td[2]/span
# EC.presence_of_element_located((By.XPATH, "//div[text()='" + date + "']//parent::td//parent::tr//td[2]//div/div[5][@class='opponent-tricode']")))
# EC.presence_of_element_located((By.XPATH, "//div[text()='" + date + "']//parent::td//parent::tr//td[2]//div/div[5][@class='opponent-tricode']")))



# In[ ]:


# Extra code trying to figure out tricode looping. 
    # EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/div/div/section/section/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[2]/td[1]/span/span/span[1]/span[3]/a")))       
#EC.presence_of_element_located((By.XPATH, "//a[@class='team p-text-link--mlb")))
                                #EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/div/div/section/section/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[2]/td[1]/span/span/span[1]/span[3]/a[text()='CIN']")))  

# trying to look up by MIL LAD, etc and then manuvering to wins and losses. 
    # can you lookup by
#    me4 = driver.find_element_by_xpath("//div[@class='month-date']//parent::td//parent::tr//td[2]//div/div[5][@class='opponent-tricode']")
    
                        #      firstTeamName  = main.find_element_by_xpath("//*[@id='" + division + "']
            
            #  "//div[text()='" + date + "']//parent::td//parent::tr//td[2]//div/div[5][@class='opponent-tricode']"
            #  EC.presence_of_element_located((By.XPATH, "//div[text()='" + key + "']")))
        #print (main.get_property('text'))    
        #print (main.get_attribute("class"))
#        print (main.get_attribute("href"))
#        print (main.get_attribute("data-team-name"))
        
        #"//div[text()='" + date + "']//parent::td//parent::tr//td[2]//div/div[5][@class='opponent-tricode']")))
        #print (main.find_element_by_class_name("p-text-link--mlb"))
           # EC.presence_of_element_located((By.XPATH, "/html/body/main/div[2]/div/div/div/section/section/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[1]/td[1]/span/span/span[1]/span[3]/a")))
        #    /html/body/main/div[2]/div/div/div/section/section/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[1]/td[1]/span/span/span[1]/span[3]/a
        #/html/body/main/div[2]/div/div/div/section/section/div[2]/div[2]/div/div/div[1]/div/table/tbody/tr[2]/td[1]/span/span/span[1]/span[3]/a
        #print (team_dict)
        #TeamName  = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[1]/span/span/a")
        #Wins      = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[2]/span")
        #Losses    = main.find_element_by_xpath("//*[@id='" + division + "']//div//div//div[1]//div//table/tbody//tr[1]//td[3]/span")
        #
         #current_records_dict = {firstTeamName.get_attribute("data-team-name"):
         #                           {firstWins.text: firstLosses.text}, 
         #                       secondTeamName.get_attribute("data-team-name"):
         #                           {secondWins.text: secondLosses.text}
         #                      }
 #print (TeamName)                                               

