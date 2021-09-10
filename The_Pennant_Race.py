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
