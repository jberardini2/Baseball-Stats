#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

class BP_Stat_Class:
    def __init__(self):
        self.team_list = ()
        
    
    # **************************************** Team List *******************************************
    def getTeamList(self):
        # The team list was not queried to save on performance.
        
        team_list = ['Angels','As','Astros','Blue Jays','Braves','Brewers','Cardinals','Cubs','Dbacks','Dodgers','Giants','Indians','Mariners','Marlins','Mets','Nationals','Orioles','Padres','Phillies','Pirates','Rangers','Rays','Red Sox','Reds','Rockies','Royals','Tigers','Twins','White Sox','Yankees']
        
        return team_list
    
    # **************************************** Team List *******************************************
    def getFullTeamName(self, t):
        self.team_name = t
        # Returns the full team name with city.
             
        team_name_dict = {'Angels':'Los Angeles Angels','As':'Oakland As','Astros':'Houston Astros','Blue Jays': 'Toronto Blue Jays','Braves':'Atlanta Braves','Brewers':'Milwaukee Brewers','Cardinals':'St Louis Cardinals','Cubs':'Chicago Cubs','Dbacks':'Arizona Diamondbacks','Dodgers':'Los Angeles Dodgers','Giants': 'San Francisco Giants','Indians': 'Cleveland Indians','Mariners':'Seattle Mariners','Marlins':'Miami Marlins','Mets':'New York Mets','Nationals':'Washington Nationals','Orioles':'Baltimore Orioles','Padres': 'San Diego Padres','Phillies':'Philadelphia Phillies','Pirates':'Pittsburgh Pirates','Rangers': 'Texas Rangers','Rays':'Tampa Bay Rays','Red Sox':'Boston Red Sox','Reds':'Cincinnati Reds','Rockies':'Colorado Rockies','Royals':'Kansas City Royals','Tigers':'Detroit Tigers','Twins':'Minnesota Twins','White Sox':'Chicago White Sox','Yankees':'New York Yankess'}

        if self.team_name in team_name_dict:
            full_team_name = team_name_dict[self.team_name]
        
        return full_team_name
    
    # ************************ Get Active Roster ***************************************************
    def getActiveRoster(self, t):
        self.team = t.lower()
        
        from datetime import datetime
        import time
        start = datetime.now()
        
        active_roster_dict = {}
        active_roster_list_of_dict = []
        
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        # https://www.mlb.com/dodgers/roster
        print (self.team)
        #self.team.replace(" ", "") # need to remove spaces
        driver.get("https://www.mlb.com/" + self.team.replace(" ", "") + "/roster")
         
        # Start at jersey and then find player name and their href to their stat page.
        try: 
            roster = WebDriverWait(driver,  20).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='jersey']//parent::td//a")))  
                                                                              
            players = roster.find_elements_by_xpath("//span[@class='jersey']//parent::td//a")
     
            for player in players:
                #print (player.text)
                #print (player.get_attribute("href"))
                position = roster.find_element_by_xpath('//a[text()="' + player.text + '"]//parent::td//parent::tr//parent::tbody//parent::table//thead//tr//td[1]')
                
                # dictionary of position type (pitcher, catcher, infielder or outfielder) and player name and href to player.
                active_roster_dict = {position.text: 
                                     {player.text:player.get_attribute("href")}}
                
                active_roster_list_of_dict.append(active_roster_dict)

        finally:
            pass
        
        end = datetime.now()
        duration = end - start
        print ("Total Time for Roster Retrieval:")
        print (duration)
    
        return active_roster_list_of_dict
    
    def getPitcherURL(self, n, ar):
        self.name = n # player selected in dropdown
        self.active_roster_list_of_dict = ar  # in a list in dictionary format.
    
        for roster in self.active_roster_list_of_dict:
            for key, value in roster.items():
                for name, url in value.items():
                    if name == self.name:
                        # Get the general Season Stats for the player.
                        pitcher_URL = url
                        
        return pitcher_URL
    
    def getPlayerURL(self, n, ar):
        self.name = n # player selected in dropdown
        self.active_roster_list_of_dict = ar  # in a list in dictionary format.
    
        for roster in self.active_roster_list_of_dict:
            for key, value in roster.items():
                for name, url in value.items():
                    if name == self.name:
                        # Get the general Season Stats for the player.
                        player_URL = url
                        
        return player_URL
                        
    
    def getSeasonStats(self, u):
        self.player_url = u
        self.season_stats_dict = {}
        
        from datetime import datetime
        import time
        start = datetime.now()
        
        
        
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        driver.get(self.player_url)
        
        try: 
            
            driver = WebDriverWait(driver,  20).until(                                                                
                 EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-career-gametype']"))) 
              
            season_stats = driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-career-gametype']")
            type_season_options = season_stats.find_elements_by_tag_name("option")
            for option in type_season_options:
                if option.get_attribute("innerHTML") == "Regular Season":
                    print (option.get_attribute('innerHTML'))
                    option.click()
            
            time.sleep(5)
            
            at_bats = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[5]//span")
            for ab in at_bats:
                self.season_stats_dict['AB'] = ab.text
                break

            runs = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[6]//span")
            for r in runs:
                self.season_stats_dict['R'] = r.text
                break
                
            hits = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[7]//span")
            for h in hits:
                self.season_stats_dict['H'] = h.text
                break
            
            homeruns = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[11]//span")
            for hr in homeruns:
                self.season_stats_dict['HR'] = hr.text
                break
                
            runs_batted_in = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[12]//span")
            for rbi in runs_batted_in:
                self.season_stats_dict['RBI'] = rbi.text
                break
                
            walks = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[13]//span")
            for bb in walks:
                self.season_stats_dict['BB'] = bb.text
                break
                
            strike_outs = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[15]//span")
            for so in strike_outs:
                self.season_stats_dict['SO'] = so.text
                break
            
            stolen_bases = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[16]//span")
            for sb in stolen_bases:
                self.season_stats_dict['SB'] = sb.text
                break
            
            batting_average = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[18]//span")
            for ba in batting_average:
                self.season_stats_dict['BA'] = ba.text
                break       

        finally:
            pass
        
        end = datetime.now()
        duration = end - start
        print ("Total Time for Season Stat Retrieval:")
        print (duration)
        
        return self.season_stats_dict
    
    def getLeftyStats(self, u):
        self.player_url = u
        self.season_left_handed_stats_dict = {}
        
        from datetime import datetime
        import time
        start = datetime.now()
        
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        # Open splits page 
        driver.get(self.player_url + "?stats=splits") 
                       
        try: # season left handed stats - building dictionary for return
            driver = WebDriverWait(driver, 30).until(                                                                
                 EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-splits-gametype']"))) 
              
            split_stats = driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-splits-gametype']")   
            type_season_options = split_stats.find_elements_by_tag_name("option")
            for option in type_season_options:
                if option.get_attribute("innerHTML") == "Regular Season":
                    print (option.get_attribute('innerHTML'))
                    option.click()
            
            time.sleep(5)
            
            at_bats = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[3]")
            for ab in at_bats:
                self.season_left_handed_stats_dict['AB'] = ab.text
                break
                                                    
            runs = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[4]")
            for r in runs:
                self.season_left_handed_stats_dict['R'] = r.text
                break
                
            hits = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[5]")
            for h in hits:
                self.season_left_handed_stats_dict['H'] = h.text
                break
                
            homeruns = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[8]")
            for hr in homeruns:
                self.season_left_handed_stats_dict['HR'] = hr.text
                break
                
            runs_batted_in = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[9]")
            for rbi in runs_batted_in:
                self.season_left_handed_stats_dict['RBI'] = rbi.text
                break
                
            walks =  split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[10]")
            for bb in walks:
                self.season_left_handed_stats_dict['BB'] = bb.text
                break
                
            strike_outs = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[12]")
            for so in strike_outs:
                self.season_left_handed_stats_dict['SO'] = so.text
                break
                
            stolen_bases = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[13]")
            for sb in stolen_bases:
                self.season_left_handed_stats_dict['SB'] = sb.text
                break
                
            batting_average = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[15]")
            for ba in batting_average:
                self.season_left_handed_stats_dict['BA'] = ba.text
                break

        finally:
            pass
        

        end = datetime.now()
        duration = end - start
        print ("Total Time for Left Handed StatsSeason Stat Retrieval:")
        print (duration)
        
        print ("Left Handed Stats")
        print (self.season_left_handed_stats_dict)
        return self.season_left_handed_stats_dict
 
    def getRightyStats(self, u):
        self.player_url = u
        self.season_right_handed_stats_dict = {}
        
        from datetime import datetime
        import time
        start = datetime.now()
        
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        # Open splits page 
        driver.get(self.player_url + "?stats=splits")  
        
        try: # season right handed stats - building dictionary for return
            driver = WebDriverWait(driver, 30).until(                                                                
                 EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-splits-gametype']"))) 
              
            split_stats = driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-splits-gametype']")   
            type_season_options = split_stats.find_elements_by_tag_name("option")
            for option in type_season_options:
                if option.get_attribute("innerHTML") == "Regular Season":
                    print (option.get_attribute('innerHTML'))
                    option.click()
            
            time.sleep(5)
                                                            
            at_bats = split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[3]")
            for ab in at_bats:
                self.season_right_handed_stats_dict['AB'] = ab.text
                break
                                                    
            runs = split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[4]")
            for r in runs:
                self.season_right_handed_stats_dict['R'] = r.text
                break
                
            hits = split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[5]")
            for h in hits:
                self.season_right_handed_stats_dict['H'] = h.text
                break
            
            homeruns = split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[8]")
            for hr in homeruns:
                self.season_right_handed_stats_dict['HR'] = hr.text
                break
             
            runs_batted_in = split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[9]")
            for rbi in runs_batted_in:
                self.season_right_handed_stats_dict['RBI'] = rbi.text
                break
                
            walks =  split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[10]")
            for bb in walks:
                self.season_right_handed_stats_dict['BB'] = bb.text
                break
                
            strike_outs = split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[12]")
            for so in strike_outs:
                self.season_right_handed_stats_dict['SO'] = so.text
                break
                        
            stolen_bases = split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[13]")
            for sb in stolen_bases:
                self.season_right_handed_stats_dict['SB'] = sb.text
                break
            
            batting_average = split_stats.find_elements_by_xpath("//span[text()='vs. Right']//parent::td/following-sibling::td[15]")
            for ba in batting_average:
                self.season_right_handed_stats_dict['BA'] = ba.text
                break

        finally:
            pass
        
        end = datetime.now()
        duration = end - start
        print ("Total Time for Right Handed Stats:")
        print (duration)
        
        print ("Right Handed Stats")
        print (self.season_right_handed_stats_dict)
        return self.season_right_handed_stats_dict
        
    def getPitcherVersusBatterStats(self, u , p, t):
        player_url = u
        pitcher_url = p
        pitcher_team_name = t
        
        from datetime import datetime
        import time
        start = datetime.now()
        
        from selenium.common.exceptions import NoSuchElementException
    
        versus_pitcher_stats_dict = {}
        versus_pitcher_total_stats_dict = {}
        
        from datetime import datetime
        datetime_local = datetime.now()
        current_year = datetime_local.strftime('%Y')
                         
        full_team_name = self.getFullTeamName(pitcher_team_name)
        
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)

        # Open Batter versus Pitcher page - could also replace the word "pitching" with "hitting" and get the same page.
        driver.get(player_url + "?stats=bvp-r-pitching-mlb&year=" + current_year)  
        # leave code alone below and add a look up of team name in batter versus pitcher. Update team list with full name such as
        # Los Angeles Dodgers then look up by this name.
        
        # splits the url into 3 fields:  1. https://www.mlb.com/player/max 2. muncy 3, 571970
        # The third item is the unique identifier assigned to each player.
        pitcher_url_list = pitcher_url.split("-")
        
        #try: # select the batter pictcher drop down list and select the player. 
            # This xpath is from the "All Opponents Faced" dropdown after the ".get" of the "Batter vs. Pitcher"
        #    batter_versus_pitcher = WebDriverWait(driver,  20).until(                                                                
        #        EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']")))  
        try:
            driver = WebDriverWait(driver,  20).until(                                                                
                 EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-team']" ))) 
              
            teamSelection = driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-team']")
            all_teams = teamSelection.find_elements_by_tag_name("option")
            for option in all_teams:
                if option.get_attribute("innerHTML") == full_team_name:
                    print (option.get_attribute('innerHTML'))
                    option.click()

            time.sleep(5)
            # 
            batter_versus_pitcher = teamSelection.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']")

            option_list = batter_versus_pitcher.find_elements_by_tag_name("option")
            
            for option in option_list:
                #print("Value is: %s" % option.get_attribute("value"))
                # match web page dropdown list selection to number from url.
                if option.get_attribute("value") == pitcher_url_list[2]:
                    option.click()  # select item to view relevant stats
                    
                    time.sleep(1) 
            
                    at_bats = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[3]/span")
                    versus_pitcher_stats_dict['AB'] = at_bats.text

                    runs = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[4]/span") 
                    versus_pitcher_stats_dict['R'] = runs.text
            
                    hits = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[5]/span") 
                    versus_pitcher_stats_dict['H'] = hits.text

                    homeruns = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[8]/span") 
                    versus_pitcher_stats_dict['HR'] = homeruns.text

                    runs_batted_in = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[9]/span") 
                    versus_pitcher_stats_dict['RBI'] = runs_batted_in.text

                    walks = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[10]/span") 
                    versus_pitcher_stats_dict['BB'] = walks.text

                    strike_outs = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[12]/span")  
                    versus_pitcher_stats_dict['SO'] = strike_outs.text

                    stolen_bases = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[13]/span")  
                    versus_pitcher_stats_dict['SB'] = stolen_bases.text

                    batting_average = batter_versus_pitcher.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[15]/span")  
                    versus_pitcher_stats_dict['BA'] = batting_average.text
                        
                    # Career totals against pitcher:
            
        except NoSuchElementException as ex:
            print("Pitcher Versus Batter Exception has been thrown. " + str(ex))
    
        try:
            
                    total_at_bats = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[3]/span")  
                    versus_pitcher_total_stats_dict['AB'] = total_at_bats.text

                    total_runs = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[4]/span") 
                    versus_pitcher_total_stats_dict['R'] = total_runs.text

                    total_hits = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[5]/span") 
                    versus_pitcher_total_stats_dict['H'] = total_hits.text

                    total_homeruns = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[8]/span") 
                    versus_pitcher_total_stats_dict['HR'] = total_homeruns.text

                    total_runs_batted_in = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[9]/span") 
                    versus_pitcher_total_stats_dict['RBI'] = total_runs_batted_in.text

                    total_walks = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[10]/span") 
                    versus_pitcher_total_stats_dict['BB'] = total_walks.text

                    total_strike_outs = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[12]/span")  
                    versus_pitcher_total_stats_dict['SO'] = total_strike_outs.text

                    total_stolen_bases = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[13]/span")  
                    versus_pitcher_total_stats_dict['SB'] = total_stolen_bases.text

                    total_batting_average = batter_versus_pitcher.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[15]/span")  
                    versus_pitcher_total_stats_dict['BA'] = total_batting_average.text

        finally:
            pass
        
        end = datetime.now()
        duration = end - start
        print ("Total Time for Pitcher versus Batter Stats:")
        print (duration)
        
        return versus_pitcher_stats_dict, versus_pitcher_total_stats_dict

    
from tkinter import *
from PIL import ImageTk,Image
# https://pythonguides.com/python-tkinter-optionmenu/
root = Tk()
root.title("Batter versus Pitcher")
root.geometry("1200x1200")

FrameIt=Frame(root)
FrameIt.grid(padx = 200, pady = 200)

BP = BP_Stat_Class()
Def_Team_List = BP.getTeamList()
Def_Team_List.insert(0,"Select Pitcher's Team")

Off_Team_List = BP.getTeamList()
Off_Team_List.insert(0,"Select Batter's Team")

Pitcher_List = ["------"]   
Batter_List = ["------"]   


# Create a Tkinter variable
tk_Def_Team = StringVar(root)
tk_Pitcher  = StringVar(root)
tk_Off_Team = StringVar(root)
tk_Batter   = StringVar(root)

label_Def = Label(root, text="Defense Team/Pitcher")
label_Def.grid(row=1, column=0, sticky='n')
label_Def.config(width = 20)
label_Def.config(bg="GREEN", fg="WHITE")


label_Off = Label(root, text="Offensive Team/Hitter")
label_Off.grid(row=5, column=0, sticky='n')
label_Off.config(width = 20)
label_Off.config(bg="DARK BLUE", fg="WHITE")


#label_separation_1 = Label(root, text="\t\t\t")
#label_separation_1.grid(row=3, column=0, sticky='n')

drop_Def_Team = OptionMenu(root, tk_Def_Team, *Def_Team_List)
tk_Def_Team.set(Def_Team_List[0])
drop_Def_Team.config(width = 20)
drop_Def_Team.config(bg="GREEN", fg="WHITE")
drop_Def_Team["menu"].config(bg="GREEN", fg="WHITE")
#drop_Def_Team.grid(row=3, column=5, sticky='n')
drop_Def_Team.grid(row=2, column=0, sticky='n')

drop_Pitcher = OptionMenu(root, tk_Pitcher, *Pitcher_List)
tk_Pitcher.set(Pitcher_List[0])
drop_Pitcher.config(width = 20)
drop_Pitcher.config(bg="GREEN", fg="WHITE")
drop_Pitcher["menu"].config(bg="GREEN", fg="WHITE")
drop_Pitcher.grid(row=3, column=0, sticky='n')
#drop_Pitcher.grid(row=3, column=10, sticky='n')

label_separation_2 = Label(FrameIt, text="\t\t\t")
label_separation_2.grid(row=4, column=0, sticky='n')

drop_Off_Team = OptionMenu(root, tk_Off_Team, *Off_Team_List)
tk_Off_Team.set(Off_Team_List[0])
drop_Off_Team.config(width = 20)
drop_Off_Team.config(bg="DARK BLUE", fg="WHITE")
drop_Off_Team["menu"].config(bg="DARK BLUE", fg="WHITE")
drop_Off_Team.grid(row=6, column=0, sticky='n')
#drop_Off_Team.grid(row=3, column=20, sticky='n')

drop_Batter = OptionMenu(root, tk_Batter, *Batter_List)
tk_Batter.set(Batter_List[0])
drop_Batter.config(width = 20)
drop_Batter.config(bg="DARK BLUE", fg="WHITE")
drop_Batter["menu"].config(bg="DARK BLUE", fg="WHITE")
drop_Batter.grid(row=7, column=0, sticky='n')
#drop_Batter.grid(row=3, column=25, sticky='n')

label_separation_2 = Label(root, text="\t\t\t")
label_separation_2.grid(row=8, column=0, sticky='n')


#label_separation_3 = Label(root, text="\t\t\t")
#label_separation_3.grid(row=5, column=5, sticky='n')

# on change dropdown value
def change_Def_Team_dropdown(*args):
    global g_selected_Def_Team
    g_selected_Def_Team = str(tk_Def_Team.get())
    print(g_selected_Def_Team)
    global g_def_roster_list_of_dict
    g_def_roster_list_of_dict = []
    g_def_roster_list_of_dict = BP.getActiveRoster(g_selected_Def_Team)
    print ("*************************************")
    print (g_def_roster_list_of_dict)
    print ("*************************************")
    drop_Pitcher.children["menu"].delete(0, "end")
    filtered_pitcher_roster_list = []
    for roster in g_def_roster_list_of_dict:
        for key, value in roster.items():
            
            if key == "Pitchers":
                for name, url in value.items():
                    filtered_pitcher_roster_list.append(name)
                    drop_Pitcher.children["menu"].add_command(label=name, command=lambda varName=name: tk_Pitcher.set(varName)) 
    tk_Pitcher.set(filtered_pitcher_roster_list[0])
        
    
def change_Pitcher_dropdown(*args):
    global g_selected_Pitcher
    g_selected_Pitcher = str(tk_Pitcher.get())
    print(g_selected_Pitcher)
    

def change_Off_Team_dropdown(*args):
    global g_selected_Off_Team
    g_selected_Off_Team = str(tk_Off_Team.get())
    print ("*************************************")
    print(g_selected_Off_Team)
    print ("*************************************")
    global g_off_roster_list_of_dict
    g_off_roster_list_of_dict = []
    g_off_roster_list_of_dict = BP.getActiveRoster(g_selected_Off_Team)
    print (g_off_roster_list_of_dict)
    
    drop_Batter.children["menu"].delete(0, "end")
    filtered_batter_roster_list = []
    for roster in g_off_roster_list_of_dict:
        for key, value in roster.items():
            
            if key == "Catchers" or key == "Infielders" or key == "Outfielders":
                for name, url in value.items():
                    filtered_batter_roster_list.append(name)
                    drop_Batter.children["menu"].add_command(label=name, command=lambda varName=name: tk_Batter.set(varName)) 
    tk_Batter.set(filtered_batter_roster_list[0])

    
def change_Batter_dropdown(*args):
    global g_selected_Batter
    g_selected_Batter = str(tk_Batter.get())
    print(g_selected_Batter)


def process(*args):

    url = ""
    # I had a strange issue where the player url was switching to Chris Taylor who is last in the dictionary list. 
    
    # remove labels and anything else within the frame before writing new information about a player.
    for item in FrameIt.winfo_children():
        item.destroy()

    url = BP.getPlayerURL(g_selected_Batter, g_off_roster_list_of_dict )
    season_stats_dict = BP.getSeasonStats(url)
    
    print (season_stats_dict)
    label_line = Label(FrameIt, text= "Player: " + g_selected_Batter, font='bold')
    label_line.grid(row=3, column=10, sticky='e')
    label_line = Label(FrameIt, text= "Season Stats: ")
    label_line.grid(row=4, column=10, sticky='e')
    # row 5 and 10 and 6 and 10
    v_col = 10
    # print out season stats to tkinter display
    for key in season_stats_dict:
        label_line = Label(FrameIt, text= key + "\t")
        label_line.grid(row=5, column=v_col, sticky='e')
        label_line = Label(FrameIt, text= season_stats_dict[key] + "\t")
        label_line.grid(row=6, column=v_col, sticky='e')
        v_col += 1
        
    # ************* Season left handed stats ******************************
    # Calling routine to get player URL again because of issue.
    player_url = BP.getPlayerURL(g_selected_Batter, g_off_roster_list_of_dict )
    lefty_stat_dict = BP.getLeftyStats(player_url)
    
    label_line = Label(FrameIt, text= "Season Left Handed Stats: ")
    label_line.grid(row=10, column=10, sticky='e')
    # row 5 and 10 and 6 and 10
    v_col = 10
    # print out season stats to tkinter display
 
    for key in lefty_stat_dict:
        label_line = Label(FrameIt, text= key + "\t")
        label_line.grid(row=11, column=v_col, sticky='e')
        label_line = Label(FrameIt, text= lefty_stat_dict[key] + "\t")
        label_line.grid(row=12, column=v_col, sticky='e')
        v_col += 1
        
    # ************* Season right handed stats ******************************
    # Calling routine to get player URL again because of issue.
    batter_url = BP.getPlayerURL(g_selected_Batter, g_off_roster_list_of_dict)
    righty_stat_dict = BP.getRightyStats(batter_url)
    
    label_line = Label(FrameIt, text= "Season Right Handed Stats: ")
    label_line.grid(row=14, column=10, sticky='e')
    
    v_col = 10
    # print out season stats to tkinter display
    for key in righty_stat_dict:
        
        label_line = Label(FrameIt, text= key + "\t")
        label_line.grid(row=15, column=v_col, sticky='e')
        label_line = Label(FrameIt, text=  righty_stat_dict[key] + "\t")
        label_line.grid(row=16, column=v_col, sticky='e')
        v_col += 1
    
     # ************* Season against pitcher and for totals against pitcher for career  *********************
    pitcher_url = BP.getPitcherURL(g_selected_Pitcher, g_def_roster_list_of_dict) 
    pitcher_stats_dict, pitcher_total_stats_dict = BP.getPitcherVersusBatterStats(batter_url, pitcher_url, g_selected_Def_Team)
    
    label_line = Label(FrameIt, text= "Season Versus: " + g_selected_Pitcher).grid(row=20, column=10, sticky='e')
    
    v_col = 10
    # print out season stats to tkinter display
    for key in pitcher_stats_dict:
        label_line = Label(FrameIt, text= key + "\t")
        label_line.grid(row=21, column=v_col, sticky='e')
        label_line = Label(FrameIt, text=  pitcher_stats_dict[key] + "\t")
        label_line.grid(row=22, column=v_col, sticky='e')
        v_col += 1
    label_line = Label(FrameIt, text= "Career Versus: " + g_selected_Pitcher)
    label_line.grid(row=24, column=10, sticky='e')
    
    v_col = 10
    # print out season stats to tkinter display
    for key in pitcher_total_stats_dict:
        
        label_line = Label(FrameIt, text= key + "\t")
        label_line.grid(row=25, column=v_col, sticky='e')
        label_line = Label(FrameIt, text=  pitcher_total_stats_dict[key] + "\t")
        label_line.grid(row=26, column=v_col, sticky='e')
        v_col += 1
            
    
    print (pitcher_stats_dict)
    print (pitcher_total_stats_dict)
    
    
    
button_process = Button(root, text="Process",command=process, padx = 50, fg="blue")  #padx = 50, pady = 50 command=process() to process immediately
button_process.config(width = 20)
button_process.config(bg="GREY", fg="WHITE")
button_process.grid(row=9, column=0, sticky='n')

   
# link function to change dropdown
tk_Def_Team.trace('w', change_Def_Team_dropdown)

# link function to change dropdown
tk_Pitcher.trace('w', change_Pitcher_dropdown)

tk_Off_Team.trace('w', change_Off_Team_dropdown)

# link function to change dropdown
tk_Batter.trace('w', change_Batter_dropdown)

   
root.mainloop()


# In[ ]:


# SEASON STAT EXPERIMENT TRYING TO GRAB THE ENTIRE ROW.  THEN PARSE IN PYTHON.
# Selenium Getting data from MLB/standings
from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lxml.html

from datetime import datetime
import time
start = datetime.now()
  
season_stats_dict = {}
      
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.mlb.com/player/max-muncy-571970?stats=career-r-hitting-mlb&year=2021")
      
try: 
          
  driver = WebDriverWait(driver,  5).until(                                                                
      EC.presence_of_element_located((By.XPATH, "//tr[@data-index='5']"))) 
  
  all_rows = driver.find_elements_by_tag_name("td")
  
  for row in all_rows:
      cells = row.find_elements_by_tag_name("span")
      
      for cel in cells:
          print (cel.text)
      
  
finally:
  pass

end = datetime.now()
duration = end - start
print ("Total Duration Querying Season Stats:")
print (duration)

print (type(driver))


"""   
  
  time.sleep(5)
          
      at_bats = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[5]//span")
      for ab in at_bats:
          self.season_stats_dict['AB'] = ab.text
              break

          runs = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[6]//span")
          for r in runs:
              self.season_stats_dict['R'] = r.text
              break
              
          hits = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[7]//span")
          for h in hits:
              self.season_stats_dict['H'] = h.text
              break
          
          homeruns = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[11]//span")
          for hr in homeruns:
              self.season_stats_dict['HR'] = hr.text
              break
              
          runs_batted_in = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[12]//span")
          for rbi in runs_batted_in:
              self.season_stats_dict['RBI'] = rbi.text
              break
              
          walks = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[13]//span")
          for bb in walks:
              self.season_stats_dict['BB'] = bb.text
              break
              
          strike_outs = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[15]//span")
          for so in strike_outs:
              self.season_stats_dict['SO'] = so.text
              break
          
          stolen_bases = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[16]//span")
          for sb in stolen_bases:
              self.season_stats_dict['SB'] = sb.text
              break
          
          batting_average = season_stats.find_elements_by_xpath("//span[text()='2021']//parent::td//parent::tr//td[18]//span")
          for ba in batting_average:
              self.season_stats_dict['BA'] = ba.text
              break       

      finally:
          pass
      
      return self.season_stats_dict
"""


# In[ ]:




# Selenium Getting data from MLB/standings
from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#import time

PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.mlb.com/player/corey-seager-608369?stats=splits-r-hitting-mlb&year=2021")

season_left_handed_stats_dict = {}

try: # season left handed stats - building dictionary for return
    split_stats = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='vs. Left']//parent::td/following-sibling::td[3]")))  
    
    at_bats = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[3]"")
    for ab in at_bats:
        season_left_handed_stats_dict['AB'] = ab.text
                                                    
    runs = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[4]")
    for r in runs:
        season_left_handed_stats_dict['R'] = r.text
                
    hits = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[5]")
    for h in hits:
        season_left_handed_stats_dict['H'] = h.text
            
    homeruns = split_stats.find_elements_by_xpath("//span[text()='vs. Left']//parent::td/following-sibling::td[8]")
    for hr in homeruns:
        season_left_handed_stats_dict['HR'] = hr.text
             
    runs_batted_in = split_stats.find_elements_by_xpath("//div[@id='splitsTable']/div/div/div[1]/div/table/tbody/tr[15]/td[10]/span")
    for rbi in runs_batted_in:
        season_left_handed_stats_dict['RBI'] = rbi.text
                
    walks =  split_stats.find_elements_by_xpath("//div[@id='splitsTable']/div/div/div[1]/div/table/tbody/tr[15]/td[11]/span")
    for bb in walks:
        season_left_handed_stats_dict['BB'] = bb.text
                
    strike_outs = split_stats.find_elements_by_xpath("//div[@id='splitsTable']/div/div/div[1]/div/table/tbody/tr[15]/td[13]/span")
    for so in strike_outs:
        season_left_handed_stats_dict['SO'] = so.text
                        
    stolen_bases = split_stats.find_elements_by_xpath("//div[@id='splitsTable']/div/div/div[1]/div/table/tbody/tr[15]/td[14]/span")
    for sb in stolen_bases:
        season_left_handed_stats_dict['SB'] = sb.text
            
    batting_average = split_stats.find_elements_by_xpath("//div[@id='splitsTable']/div/div/div[1]/div/table/tbody/tr[15]/td[16]/span")
    for ba in batting_average:
        season_left_handed_stats_dict['BA'] = ba.text

finally:
    pass

print (season_left_handed_stats_dict)    


# In[ ]:



    
from tkinter import *
root = Tk()
root.title("Batter versus Pitcher")
root.geometry("900x1200")

app=Frame(root)
app.grid(padx = 200, pady = 200)
label_line = Label(app, text= "LINE 1",bd=1,relief="solid",justify=RIGHT)
label_line.grid()
label_line = Label(app, text= "LINE 2",bd=1,relief="solid",justify=RIGHT)
label_line.grid()
label_line = Label(app, text= "LINE 3",bd=1,relief="solid",justify=RIGHT)
label_line.grid()
label_line = Label(app, text= "LINE 4",bd=1,relief="solid",justify=RIGHT)
label_line.grid()
label_line = Label(app, text= "LINE 5",bd=1,relief="solid",justify=RIGHT)
label_line.grid()

lbl = Label(app, text = "I'm a label!")
lbl.grid()



def process(*args):
    
    for item in app.winfo_children():
        item.destroy()
    
    #label_line.destroy()
    
def add_stuff(*args):
    
    label_line = Label(app, text= "LINE 6",bd=1,relief="solid",justify=RIGHT)
    label_line.grid()
    label_line = Label(app, text= "LINE 7",bd=1,relief="solid",justify=RIGHT)
    label_line.grid()
    label_line = Label(app, text= "LINE 8",bd=1,relief="solid",justify=RIGHT)
    label_line.grid()
    label_line = Label(app, text= "LINE 9",bd=1,relief="solid",justify=RIGHT)
    label_line.grid()
    label_line = Label(app, text= "LINE 10",bd=1,relief="solid",justify=RIGHT)


button_process = Button(root, text="Process",command=process, padx = 50, fg="blue")
button_process.grid()

button_add_stuff = Button(root, text="Add Stuff",command=add_stuff, padx = 50, fg="blue")
button_add_stuff.grid()
    
 #   label_line = Label(app, text= "LINE 5",bd=1,relief="solid",justify=LEFT).grid(row=18, column=10, sticky='e')
  #  label_line = Label(app, text= "LINE 6",bd=1,relief="solid",justify=LEFT).grid(row=21, column=10, sticky='e')
     


#lbl.destroy()

#app.grid(padx = 200, pady = 200)


#app.grid(padx = 200, pady = 200)

#.grid(row=5, column=10, sticky='e')
#lbl1 = Label(app, text= "T",bd=1,relief="solid")

#app.grid()


#label_line = Label(root, text= "LIN 4",bd=1,relief="solid",justify=LEFT).grid(row=1, column=10, sticky='w')
#label = Label(frame2, text="test").pack()

#label1 = Label(, text="Left column")
#label1.pack()


root.mainloop()
    


# In[ ]:


sentence = ' hello  apple'
sentence.replace(" ", "")


# In[ ]:



from tkinter import *
root = Tk()
root.title("Batter versus Pitcher")
#root.geometry("1200x1200")
# DESTROY DOES NOT WORK FOR THIS! DON'T USE IT!
#global label_line
label_line = Label(root)


def process(*args):

global label_line
label_line = Label(root)
label_line.destroy()
label_line = Label(root, text= "LINE 5",bd=1,relief="solid",justify=LEFT).grid(row=18, column=10, sticky='e')
label_line = Label(root, text= "LINE 6",bd=1,relief="solid",justify=LEFT).grid(row=21, column=10, sticky='e')
 


def clear_all(*args):
#label_line['state'] = DISABLED
#label_clear = Label(root, text= "\t\t\t\t\t\t\t\t\t\t\t ").grid(row=18, column=10, sticky='e')
#label_clear = Label(root, text= "\t\t\t\t\t\t\t\t\t\t\t ").grid(row=19, column=10, sticky='e')
#label_clear = Label(root, text= "\t\t\t\t\t\t\t\t\t\t\t ").grid(row=20, column=10, sticky='e')
#label_clear = Label(root, text= "\t\t\t\t\t\t\t\t\t\t\t ").grid(row=21, column=10, sticky='e')
global label_line
label_line = Label(root)
label_line.after(1000, label_line.destroy())
#label_line.destroy()
#label_line['state'] = DISABLED
#label_line.grid_forget()
   # print ("here")



#button_process = Button(root, text="Process",command=process, padx = 50, fg="blue")  #padx = 50, pady = 50 command=process() to process immediately
#button_process.config(width = 20)
#button_process.config(bg="GREY", fg="WHITE")
#button_process.grid(row=9, column=0, sticky='n')

#button_clear_all = Button(root, text="Clear",command=clear_all, padx = 50, fg="blue")  #padx = 50, pady = 50 command=process() to process immediately
#button_clear_all.config(width = 20)
#button_clear_all.config(bg="GREY", fg="WHITE")
#button_clear_all.grid(row=15, column=0, sticky='n')

#label_line = Label(root, text= "LIN 1",bd=1,relief="solid",justify=LEFT).grid(row=18, column=10, sticky='w')
#label_line = Label(root, text= "LIN 2",bd=1,relief="solid",justify=LEFT).grid(row=19, column=10, sticky='w')
#label_line = Label(root, text= "LIN 3",bd=1,relief="solid",justify=LEFT).grid(row=20, column=10, sticky='w')
#label_line = Label(root, text= "LIN 4",bd=1,relief="solid",justify=LEFT).grid(row=21, column=10, sticky='w')

frame2=Frame(root,bg = "red",width=1000,height=500,cursor = "target",relief=FLAT).grid(padx = 100, pady = 200)

label = Label(frame2, text="test").pack()


root.mainloop()


# In[ ]:


from tkinter import *

root = Tk()
root.title("Labeler")
root.geometry("1200x1200")

app = Frame()
app.grid()

app = Frame(root)
app.grid(padx = 100, pady = 200)

label_line = Label(app, text= "LINE 1",bd=1,relief="solid",justify=RIGHT).grid(row=1, column=50, sticky='e')
label_line = Label(app, text= "LINE 2",bd=1,relief="solid",justify=LEFT).grid(row=2, column=50, sticky='e')
label_line = Label(app, text= "LINE 3",bd=1,relief="solid",justify=LEFT).grid(row=3, column=50, sticky='e')
label_line = Label(app, text= "LINE 4",bd=1,relief="solid",justify=LEFT).grid(row=4, column=50, sticky='e')

#button_process = Button(root, text="Process",command=process, padx = 50, fg="blue")
#button_process.config(width = 10)
#button_process.config(bg="GREY", fg="WHITE")
#button_process.grid(row=9, column=0, sticky='n')

root.mainloop(

#app = Frame(root,width=1000,height=500)
#app.grid()
#lbl = Label(app, text = "I'm a label!")
#lbl.grid()





#label = Label(frame2, text="test").pack()


#def process(*args):
    
    #global label_line
    #label_line = Label(app)
    #label_line.destroy()
    
 #   label_line = Label(app, text= "LINE 5",bd=1,relief="solid",justify=LEFT).grid(row=18, column=10, sticky='e')
  #  label_line = Label(app, text= "LINE 6",bd=1,relief="solid",justify=LEFT).grid(row=21, column=10, sticky='e')
     



#lbl = Label(app, text = "I'm a label!")
#label2 = Label(app, text= "Hey there Label!",bd=1,relief="solid")
#label_line = Label(app, text= "LIN 4",bd=1,relief="solid",justify=LEFT)
#label_line.grid(row=1, column=10, sticky='w')
#label2.grid()
#lbl.grid()


#button_process.config(width = 20)
#button_process.config(bg="GREY", fg="WHITE")
#button_process.grid(row=9, column=0, sticky='n')

)


# In[ ]:


from tkinter import *
 
root=Tk()
 
root.title("My first GUI")
 
# set resizing to false
root.resizable(width=FALSE, height=FALSE)
 
# set size of window
root.geometry('500x400')
 
leftFrame = Frame(root)
leftFrame.pack(side=LEFT)
 
rightFrame = Frame(root)
rightFrame.pack(side=RIGHT)
 
label1 = Label(leftFrame, text="Left column")
label1.pack()
 
label3 = Label(leftFrame, text="Column content")
label3.pack()
 
label2 = Label(rightFrame, text="Right column")
label2.pack()
 
# set an infinite loop so window stays in view
root.mainloop()


# In[ ]:


from tkinter import *

root = Tk()
root.geometry("400x400")

MyLabel = Label(root)

def myClick():
    global MyLabel
    myLabel = Label(root)
    
    


# In[ ]:


class C1:
    def m1(self, p):
        varp = p
        
        print (varp)

    def m2(self, a):
        var1 = a
        
        
        self.m1(var1)
        print ("all done")
        
classa = C1()

classa.m2(2)
        


# In[ ]:


# Use to time each web page.  

from datetime import datetime
import time

start = datetime.now()
time.sleep(5)
end = datetime.now()
duration = end - start

print (duration)





# In[ ]:


team_name = "Giants"
        # The full team name with city.
        
team_name_dict = {'Angels':'Los Angeles Angels','As':'Oakland As','Astros':'Houston Astros','Blue Jays': 'Toronto Blue Jays','Braves':'Atlanta Braves','Brewers':'Milwaukee Brewers','Cardinals':'St Louis Cardinals','Cubs':'Chicago Cubs','Dbacks':'Arizona Diamondbacks','Dodgers':'Los Angeles Dodgers','Giants': 'San Francisco Giants','Indians': 'Cleveland Indians','Mariners':'Seattle Mariners','Marlins':'Miami Marlins','Mets':'New York Mets','Nationals':'Washington Nationals','Orioles':'Baltimore Orioles','Padres': 'San Diego Padres','Phillies':'Philadelphia Phillies','Pirates':'Pittsburgh Pirates','Rangers': 'Texas Rangers','Rays':'Tampa Bay Rays','Red Sox':'Boston Red Sox','Reds':'Cincinnati Reds','Rockies':'Colorado Rockies','Royals':'Kansas City Royals','Tigers':'Detroit Tigers','Twins':'Minnesota Twins','White Sox':'Chicago White Sox','Yankees':'New York Yankess'}

if team_name in team_name_dict:
    print (team_name_dict[team_name])
      


# In[ ]:


#https://www.mlb.com/player/justin-turner-457759?season=2021&team=119&stats=bvp-r-hitting-mlb&year=2021
    
# Selenium Getting data from MLB/standings
from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
from selenium.webdriver.support.select import Select
#from selenium import webdriver.support.select

datetime_local = datetime.now()
current_year = datetime_local.strftime('%Y')
player_url = 'https://www.mlb.com/player/corey-seager-608369'

   
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Open Batter versus Pitcher page 
driver.get(player_url + "?stats=bvp-r-pitching-mlb&year=" + current_year)  

# select team name in list here
try:
    element = WebDriverWait(driver,  20).until(                                                                
            EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-team']" ))) 
    
    teamSelection = driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-team']")
    all_teams = teamSelection.find_elements_by_tag_name("option")
    for option in all_teams:
        
        if option.get_attribute("innerHTML") == 'San Francisco Giants':
            print (option.get_attribute('innerHTML'))
            option.click()

    time.sleep(5)
    element = teamSelection.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']")
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        #print (option.get_attribute("value"))
        print (option.get_attribute('innerHTML'))
        #if option.get_attribute("value") == '608369':
        #    option.click()
        
finally:
    pass
        
            
            


    


# In[ ]:


# model
#window_after = driver.window_handles[1]
#driver.switch_to.window(window_after)

#teamPlayerSelection = driver.window_handles[0]
#driver.switch_to.window(teamPlayerSelection)

""" 
element = driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']")
all_options = element.find_elements_by_tag_name("option")
for option in all_options:
    #print (option.get_attribute("value"))
   # print (option.get_attribute('innerHTML'))
    if option.get_attribute("value") == '608369':
        option.click()

        time.sleep(1) 
        
        versus_pitcher_stats_dict = {}
        versus_pitcher_total_stats_dict = {}
        
        at_bats = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[3]/span")
        versus_pitcher_stats_dict['AB'] = at_bats.text
        
        runs = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[4]/span") 
        versus_pitcher_stats_dict['R'] = runs.text
        
        hits = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[5]/span") 
        versus_pitcher_stats_dict['H'] = hits.text
        
        homeruns = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[8]/span") 
        versus_pitcher_stats_dict['HR'] = homeruns.text
                            
        runs_batted_in = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[9]/span") 
        versus_pitcher_stats_dict['RBI'] = runs_batted_in.text
        
        walks = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[10]/span") 
        versus_pitcher_stats_dict['BB'] = walks.text
        
        strike_outs = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[12]/span")  
        versus_pitcher_stats_dict['SO'] = strike_outs.text
        
        stolen_bases = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[13]/span")  
        versus_pitcher_stats_dict['SB'] = stolen_bases.text
        
        batting_average = element.find_element_by_xpath("//span[text()='2021']//parent::td/parent::tr/td[15]/span")  
        versus_pitcher_stats_dict['BA'] = batting_average.text
                    
        # Career totals against pitcher:
        
        total_at_bats = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[3]/span")  
        versus_pitcher_total_stats_dict['AB'] = total_at_bats.text

        total_runs = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[4]/span") 
        versus_pitcher_total_stats_dict['R'] = total_runs.text
        
        total_hits = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[5]/span") 
        versus_pitcher_total_stats_dict['H'] = total_hits.text
        
        total_homeruns = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[8]/span") 
        versus_pitcher_total_stats_dict['HR'] = total_homeruns.text
                            
        total_runs_batted_in = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[9]/span") 
        versus_pitcher_total_stats_dict['RBI'] = total_runs_batted_in.text
        
        total_walks = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[10]/span") 
        versus_pitcher_total_stats_dict['BB'] = total_walks.text
        
        total_strike_outs = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[12]/span")  
        versus_pitcher_total_stats_dict['SO'] = total_strike_outs.text
        
        total_stolen_bases = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[13]/span")  
        versus_pitcher_total_stats_dict['SB'] = total_stolen_bases.text
        
        total_batting_average = element.find_element_by_xpath("//span[text()='TOTAL']//parent::td/parent::tr/td[15]/span")  
        versus_pitcher_total_stats_dict['BA'] = total_batting_average.text

        print (versus_pitcher_stats_dict)
        print (versus_pitcher_total_stats_dict)

        
  
finally:
pass
"""     
        
    # no relation or continuation of element to at_bats to xyz  -
        #xyz = element.find_elements_by_xpath("//parent::td/parent::tr/td[3]/span") 
        
       # print (element.get_attribute('innerHTML'))
        
       # print ("*****")
        #print (type(xyz))
       #print ("*****")
        #print (xyz)
        #print ("*****")
        
        #for item in xyz:   
    
    # at_bats = WebDriverWait(driver,  20).until(                                                                
       #     EC.presence_of_element_located((By.XPATH,"//span[text()='2021']")))
                                          #((By.XPATH, )))  [1]
        #at_bats = element.find_elements_by_xpath("//span[text()='Logan Webb']")  # //td[3]//span
        #at_bats = element.find_element_by_xpath("//span[text()='2021']//ancestor::tr")  # //td[3]//span
        #at_bats = element.find_elements_by_xpath("//h3[text()='Batter vs. Pitcher']//parent::div//div//div//div//div//div//table//tbody")  #//*//span[text()='2021']
        
       
        # //span[text()='2021']//parent::td//parent::tr//td[3]//span
        # <h3 class="statistics__subheading">Batter vs. Pitcher</h3>
        # //*[@id="bvpTable"]/div/div/div[1]/div/table/tbody/tr[3]/td[3]
        #  //span[text()='2021']//parent::* This was helpful!! With find_element_by_xpath produced multiple values with at_bats.text
                               # find_elements_by_class_name("my_class")[1]
                                 # find_elements_by_class_name("my_class")[1] ANOTHER WAY TO DO QUERY
        #at_bats = element.find_elements_by_xpath("//h3[@class='statistics__subheading']")  # //td[3]//span

 


# In[ ]:


# Selenium Getting data from MLB/standings
from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
from selenium.webdriver.support.select import Select
#from selenium import webdriver.support.select

datetime_local = datetime.now()
current_year = datetime_local.strftime('%Y')
player_url = 'https://www.mlb.com/player/max-muncy-571970'

player_url_list = player_url.split("-")
print (player_url_list[0])
print (player_url_list[1])
print (player_url_list[2])
    
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Open Batter versus Pitcher page 
driver.get(player_url + "?stats=bvp-r-pitching-mlb&year=" + current_year)  

try:
    element = WebDriverWait(driver,  20).until(                                                                
            EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']")))  

    element = driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']")
    all_options = element.find_elements_by_tag_name("option")
    for option in all_options:
        print("Value is: %s" % option.get_attribute("value"))
        if option.get_attribute("value") == player_url_list[2]:
            print ("option click for: " + player_url_list[2])
            option.click()
            
finally:
    pass


# In[ ]:


player_url = 'https://www.mlb.com/player/max-muncy-571970'

player_url_list = player_url.split("-")

for item in player_url_list:
    print (item)
    
#print (player_url_list[2])


# In[ ]:













# In[ ]:


# EXCEPTION EXAMPLE

# Selenium Getting data from MLB/standings
from selenium import webdriver
# give access to keyboard keys like enter or esc.
from selenium.webdriver.common.keys import Keys
# these 3 lines below is part of the "Wait" code:
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import time
from selenium.webdriver.support.select import Select
#from selenium import webdriver.support.select

exception = TimeoutException 

datetime_local = datetime.now()
current_year = datetime_local.strftime('%Y')
player_url = 'https://www.mlb.com/player/max-muncy-571970'
    
PATH="C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Open Batter versus Pitcher page 
driver.get(player_url + "?stats=bvp-r-pitching-mlb&year=" + current_year)  

try:
    # fail fail fail!!!!!!!!!!!!!!!!!!!!!!!
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']"))).click()
    
except TimeoutException as ex:
    print("Exception has been thrown. " + str(ex))

#versus_pitcher = WebDriverWait(driver,  20).until(                                                                
#    EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu']")))  

#vp = versus_pitcher.find_elements_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']")

#driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-bvp-opponent']").click()
    
# print (type(vp))
# for v in vp:
#    print (v.text)
# print (type(versus_pitcher))

#wait.until(EC.element_to_be_clickable((By.XPATH, './/input[@id="dateRangeStart" and @name="soldDateStart"]')))
#driver.find_element_by_xpath('.//input[@id="dateRangeStart" and @name="soldDateStart"]').click()



#             EC.presence_of_element_located((By.XPATH, "//option[@value='657277']"))) ## test logan webb

#driver.find_element_by_xpath('.//option[@data-value="dateRangeStart" and @name="soldDateStart"]').click()
#driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu']").click()
#versus_pitcher = Select(driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu']"))


#time.sleep(5)

#versus_pitcher.select_by_index (5)


#start_year = Select(driver.find_element_by_xpath('.//select[@class="pika-select pika-select-year"]'))
#start_year.select_by_visible_text('2015')


#x_select.select_by_option('657277')



#//*[@id="bvp"]/ul/li[3]/div/select/option[231]
# sel = Select(driver.find_element_by_xpath
#versus_pitcher = Select(driver.find_element_by_xpath("//option[@value='657277']"))
#versus_pitcher.select_by_value("Bednar, David")
#versus_pitcher.select_by_index (5)

#             EC.presence_of_element_located((By.XPATH, "//option[@value='657277']"))) ## test logan webb
    #sel = Select(driver.find_element_by_xpath("//select[@name='continents']"))
    #versus_pitcher.select_by_value("Webb, Logan")
#versus_pitcher.click()
#Select select = new Select(customerType);
#print (versus_pitcher.text)
# versus_pitcher.select_by_visible_text("Webb, Logan")





# In[ ]:


# REMEMBER, IT WORKS LIKE THIS!!  NOT "for key, value in ...."

season_stats_dict = {'AB': '188', 'R': '26', 'H': '41', 'HR': '6', 'RBI': '22', 'BB': '20', 'SO': '53', 'SB': '0', 'BA': '.218'}

for key in season_stats_dict:
        
        print (key)
        print (season_stats_dict[key])
       # print (value)
    
    
    
        


# In[ ]:


from tkinter import *
from PIL import ImageTk,Image
from tkinter import ttk
# https://pythonguides.com/python-tkinter-optionmenu/
root = Tk()
root.title("Batter versus Pitcher")
root.geometry("1200x600")
label_explain = Label(root, text="Select all values and click process:")
#label_explain.pack()

# Create a Tkinter variable
tk_Def_Team = StringVar(root)
tk_Pitcher  = StringVar(root)
tk_Off_Team = StringVar(root)
tk_Batter   = StringVar(root)

#label_explain = Label(root, text="Select all values and click process:")
#label_explain.grid(row=1, column=15, sticky='n')

label_Def = Label(root, text="Defense Team/Pitcher")
label_Def.grid(row=1, column=0, sticky='n')
label_Def.config(width = 20)
label_Def.config(bg="GREEN", fg="WHITE")


label_Off = Label(root, text="Offensive Team/Hitter")
label_Off.grid(row=5, column=0, sticky='n')
label_Off.config(width = 20)
label_Off.config(bg="DARK BLUE", fg="WHITE")


#label_separation_1 = Label(root, text="\t\t\t")
#label_separation_1.grid(row=3, column=0, sticky='n')

Def_Team_List = ["3-10", "Padres", "Dbacks", "Rockies"]
drop_Def_Team = OptionMenu(root, tk_Def_Team, *Def_Team_List)
tk_Def_Team.set(Def_Team_List[0])
drop_Def_Team.config(width = 20)
drop_Def_Team.config(bg="GREEN", fg="WHITE")
drop_Def_Team["menu"].config(bg="GREEN", fg="WHITE")
#drop_Def_Team.grid(row=3, column=5, sticky='n')
drop_Def_Team.grid(row=2, column=0, sticky='n')

Pitcher_List = ["3-15", "Pitcher 2", "Pitcher 3"]
drop_Pitcher = OptionMenu(root, tk_Pitcher, *Pitcher_List)
tk_Pitcher.set(Pitcher_List[0])
drop_Pitcher.config(width = 20)
drop_Pitcher.config(bg="GREEN", fg="WHITE")
drop_Pitcher["menu"].config(bg="GREEN", fg="WHITE")
drop_Pitcher.grid(row=3, column=0, sticky='n')
#drop_Pitcher.grid(row=3, column=10, sticky='n')

label_separation_2 = Label(root, text="\t\t\t")
label_separation_2.grid(row=4, column=0, sticky='n')

Off_Team_List = ["3-25", "Padres", "Dbacks", "Rockies"]
drop_Off_Team = OptionMenu(root, tk_Off_Team, *Off_Team_List)
tk_Off_Team.set(Off_Team_List[0])
drop_Off_Team.config(width = 20)
drop_Off_Team.config(bg="DARK BLUE", fg="WHITE")
drop_Off_Team["menu"].config(bg="DARK BLUE", fg="WHITE")
drop_Off_Team.grid(row=6, column=0, sticky='n')
#drop_Off_Team.grid(row=3, column=20, sticky='n')

Batter_List = ["3-30", "Batter 2", "Batter 3"]
drop_Batter = OptionMenu(root, tk_Batter, *Batter_List)
tk_Batter.set(Batter_List[0])
drop_Batter.config(width = 20)
drop_Batter.config(bg="DARK BLUE", fg="WHITE")
drop_Batter["menu"].config(bg="DARK BLUE", fg="WHITE")
drop_Batter.grid(row=7, column=0, sticky='n')
#drop_Batter.grid(row=3, column=25, sticky='n')

label_separation_2 = Label(root, text="\t\t\t")
label_separation_2.grid(row=8, column=0, sticky='n')

button_process = Button(root, text="Process")
button_process.config(width = 20)
button_process.config(bg="GREY", fg="WHITE")
button_process.grid(row=9, column=0, sticky='n')
#button_process.grid(row=4, column=15, sticky='n')


label_separation_3 = Label(root, text="\t\t\t")
label_separation_3.grid(row=5, column=5, sticky='n')

label_line = Label(root, text="Player: Max Muncy", font='bold').grid(row=3, column=10, sticky='n')
label_line = Label(root, text="Season Stats: ").grid(row=4, column=10, sticky='n')

label_line = Label(root, text="463\t90\t116\t34\t88\t78\t114\t2\t.251").grid(row=5, column=10, sticky='n')
label_line = Label(root, text="AB\tR\tH\tHR\tRBI\tBB\tSO\tSB\tBA").grid(row=6, column=10, sticky='n')



root.mainloop()


# In[ ]:


g_off_roster_list_of_dict = [{'Pitchers': {'Phil Bickford': 'https://www.mlb.com/player/phil-bickford-641360'}}, {'Pitchers': {'Justin Bruihl': 'https://www.mlb.com/player/justin-bruihl-677865'}}, {'Pitchers': {'Walker Buehler': 'https://www.mlb.com/player/walker-buehler-621111'}}, {'Pitchers': {'Tony Gonsolin': 'https://www.mlb.com/player/tony-gonsolin-664062'}}, {'Pitchers': {'Brusdar Graterol': 'https://www.mlb.com/player/brusdar-graterol-660813'}}, {'Pitchers': {'Shane Greene': 'https://www.mlb.com/player/shane-greene-572888'}}, {'Pitchers': {'Kenley Jansen': 'https://www.mlb.com/player/kenley-jansen-445276'}}, {'Pitchers': {'Joe Kelly': 'https://www.mlb.com/player/joe-kelly-523260'}}, {'Pitchers': {'Clayton Kershaw': 'https://www.mlb.com/player/clayton-kershaw-477132'}}, {'Pitchers': {'Corey Knebel': 'https://www.mlb.com/player/corey-knebel-608349'}}, {'Pitchers': {'Evan Phillips': 'https://www.mlb.com/player/evan-phillips-623465'}}, {'Pitchers': {'David Price': 'https://www.mlb.com/player/david-price-456034'}}, {'Pitchers': {'Max Scherzer': 'https://www.mlb.com/player/max-scherzer-453286'}}, {'Pitchers': {'Blake Treinen': 'https://www.mlb.com/player/blake-treinen-595014'}}, {'Pitchers': {'Julio Urías': 'https://www.mlb.com/player/julio-urias-628711'}}, {'Pitchers': {'Alex Vesia': 'https://www.mlb.com/player/alex-vesia-681911'}}, {'Catchers': {'Austin Barnes': 'https://www.mlb.com/player/austin-barnes-605131'}}, {'Catchers': {'Will Smith': 'https://www.mlb.com/player/will-smith-669257'}}, {'Infielders': {'Gavin Lux': 'https://www.mlb.com/player/gavin-lux-666158'}}, {'Infielders': {'Max Muncy': 'https://www.mlb.com/player/max-muncy-571970'}}, {'Infielders': {'Albert Pujols': 'https://www.mlb.com/player/albert-pujols-405395'}}, {'Infielders': {'Corey Seager': 'https://www.mlb.com/player/corey-seager-608369'}}, {'Infielders': {'Trea Turner': 'https://www.mlb.com/player/trea-turner-607208'}}, {'Infielders': {'Justin Turner': 'https://www.mlb.com/player/justin-turner-457759'}}, {'Outfielders': {'Matt Beaty': 'https://www.mlb.com/player/matt-beaty-607461'}}, {'Outfielders': {'Mookie Betts': 'https://www.mlb.com/player/mookie-betts-605141'}}, {'Outfielders': {'Luke Raley': 'https://www.mlb.com/player/luke-raley-670042'}}, {'Outfielders': {'Chris Taylor': 'https://www.mlb.com/player/chris-taylor-621035'}}]

for roster in g_off_roster_list_of_dict:
    for key, value in roster.items():
        for name, url in value.items():
            if name == 'Max Muncy':
                print (url)


# In[ ]:


from tkinter import *
from PIL import ImageTk,Image
# https://pythonguides.com/python-tkinter-optionmenu/
root = Tk()
root.title("Batter versus Pitcher")
root.geometry("600x400")

global g_process_label


def process(*args):
   
    #process_label = Label(root, text= "Processing stats for batter versus pitcher")

   # process_label.after(1000, process_label.destroy())
    #process_label = Label(root, text= "-----")
    #process_label.pack()
   # process_label = Label(root, text= "").pack()
    g_process_label = Label(root, text= "Processing stats for batter versus pitcher")
    g_process_label.place(relx = 0.5, rely = 0.5, anchor = 'center')
    
    #g_selected_Off_Team = str(tk_Off_Team.get())
    # open players stat page with url
    # find stats
    #g_process_label.pack()

def destroy(*args):
    #process_label = Label(root, text= "-")
    #process_label.pack()
    g_process_label.destroy()
    g_process_label.pack()
    
button_process = Button(root, text="Process",command=process, padx = 50, fg="blue")  #padx = 50, pady = 50 command=process() to process immediately
button_process.pack()

button_destroy = Button(root, text="Destroy",command=destroy, padx = 70, fg="red")  #padx = 50, pady = 50 command=process() to process immediately
button_destroy.pack()
   
root.mainloop()


# In[ ]:


row = 5

row += 1

print (row)


# In[ ]:


dict = {'Phil Bickford': 'https://www.mlb.com/player/phil-bickford-641360'}


for key in dict:
    print (value)


# In[ ]:



global first_time
first_time = True

if not first_time:
    first_time = False
    
    
print (first_time)


# In[ ]:


from tkinter import *

root = Tk()
root.title("Calculate")

# Create a Tkinter variable
tkvar = StringVar(root)

# Dictionary with options
choices = sorted({'Good', 'Bad', 'Medium'})
tkvar.set('Good')  # set the default option

popupMenu = OptionMenu(root, tkvar, *choices)
Label(root, text="Please choose").grid(row=2, column=2)
popupMenu.grid(row=3, column=2)
b2 = Button(root, text='Close', command=root.quit)
b2.grid(row=6, column=2)

# on change dropdown value
def change_dropdown(*args):
    global dropdown
    dropdown = str(tkvar.get())
    print(dropdown)

    if tkvar.get() == 'Good':
        print(5)

    if tkvar.get() == "Bad":
        print(10)

# link function to change dropdown
tkvar.trace('w', change_dropdown)

root.mainloop()


# In[ ]:


#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tkinter as tk
 
window = tk.Tk()
window.title('My Window')
 
window.geometry('500x300')
 
var1 = tk.StringVar()
l = tk.Label(window, bg='green', fg='yellow',font=('Arial', 12), width=10, textvariable=var1)
l.pack()
 
def print_selection():
    value = lb.get(lb.curselection())   
    var1.set(value)  
 
b1 = tk.Button(window, text='print selection', width=15, height=2, command=print_selection)
b1.pack()
 
var2 = tk.StringVar()
var2.set((1,2,3,4))
lb = tk.Listbox(window, listvariable=var2)

list_items = ["Dodgers", "Giants", "Reds", "Padres", "Brewers","Dodgers", "Giants", "Reds", "Padres", "Brewers","Dodgers", "Giants", "Reds", "Padres", "Brewers","Dodgers", "Giants", "Reds", "Padres", "Brewers","Dodgers", "Giants", "Reds", "Padres", "Brewers","Dodgers", "Giants", "Reds", "Padres", "Brewers","Dodgers", "Giants", "Reds", "Padres", "Brewers"]
for item in list_items:
    lb.insert('end', item)
lb.insert(1, 'first')
lb.insert(2, 'second')
lb.delete(2)
lb.pack()
 
window.mainloop()


# In[ ]:




