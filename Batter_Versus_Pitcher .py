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
        
        current_year = start.strftime('%Y')
        
        
        
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
            
            time.sleep(10)
            
            at_bats = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[5]//span")
            for ab in at_bats:
                self.season_stats_dict['AB'] = ab.text
                break

            runs = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[6]//span")
            for r in runs:
                self.season_stats_dict['R'] = r.text
                break
                
            hits = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[7]//span")
            for h in hits:
                self.season_stats_dict['H'] = h.text
                break
            
            homeruns = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[11]//span")
            for hr in homeruns:
                self.season_stats_dict['HR'] = hr.text
                break
                
            runs_batted_in = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[12]//span")
            for rbi in runs_batted_in:
                self.season_stats_dict['RBI'] = rbi.text
                break
                
            walks = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[13]//span")
            for bb in walks:
                self.season_stats_dict['BB'] = bb.text
                break
                
            strike_outs = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[15]//span")
            for so in strike_outs:
                self.season_stats_dict['SO'] = so.text
                break
            
            stolen_bases = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[16]//span")
            for sb in stolen_bases:
                self.season_stats_dict['SB'] = sb.text
                break
            
            batting_average = season_stats.find_elements_by_xpath("//span[text()=" + current_year + "]//parent::td//parent::tr//td[18]//span")
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
        
        # select the batter pictcher drop down list and select the player. 
        # This xpath is from the "All Opponents Faced" dropdown after the ".get" of the "Batter vs. Pitcher"
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
            
                    at_bats = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[3]/span")
                    versus_pitcher_stats_dict['AB'] = at_bats.text

                    runs = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[4]/span") 
                    versus_pitcher_stats_dict['R'] = runs.text
            
                    hits = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[5]/span") 
                    versus_pitcher_stats_dict['H'] = hits.text

                    homeruns = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[8]/span") 
                    versus_pitcher_stats_dict['HR'] = homeruns.text

                    runs_batted_in = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[9]/span") 
                    versus_pitcher_stats_dict['RBI'] = runs_batted_in.text

                    walks = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[10]/span") 
                    versus_pitcher_stats_dict['BB'] = walks.text

                    strike_outs = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[12]/span")  
                    versus_pitcher_stats_dict['SO'] = strike_outs.text

                    stolen_bases = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[13]/span")  
                    versus_pitcher_stats_dict['SB'] = stolen_bases.text

                    batting_average = batter_versus_pitcher.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[15]/span")  
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

    def getPostSeasonStats(self, u):
        player_url = u
        
        from datetime import datetime
        import time
        start = datetime.now()
        
        from selenium.common.exceptions import NoSuchElementException
    
        post_season_year_dict = {}
        post_season_career_dict = {}
        
        from datetime import datetime
        datetime_local = datetime.now()
        current_year = datetime_local.strftime('%Y')
                         
        PATH="C:\Program Files (x86)\chromedriver.exe"
        driver = webdriver.Chrome(PATH)
        # for postseason https://www.mlb.com/player/corey-seager-608369?stats=career-p-hitting-mlb&year=2021
        driver.get(player_url + "?stats=career-p-hitting-mlb&year=" + current_year)  
        
        try: 
            
            driver = WebDriverWait(driver,  20).until(                                                                
                 EC.presence_of_element_located((By.XPATH, "//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-career-gametype']"))) 
              
            postseason_stats = driver.find_element_by_xpath("//select[@class='p-dropdown__actual-select-element dropdown-menu' and @aria-labelledby='type-career-gametype']")
            type_season_options = postseason_stats.find_elements_by_tag_name("option")
            for option in type_season_options:
                if option.get_attribute("innerHTML") == "Postseason Cumulative":
                    print (option.get_attribute('innerHTML'))
                    option.click()
            
            time.sleep(5)
            
            # get postseason current year stats.  
            at_bats = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[5]/span")
            post_season_year_dict['AB'] = at_bats.text

            runs = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[6]/span") 
            post_season_year_dict['R'] = runs.text
            
            hits = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[7]/span") 
            post_season_year_dict['H'] = hits.text

            homeruns = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[11]/span") 
            post_season_year_dict['HR'] = homeruns.text

            runs_batted_in = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[12]/span") 
            post_season_year_dict['RBI'] = runs_batted_in.text

            walks = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[13]/span") 
            post_season_year_dict['BB'] = walks.text

            strike_outs = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[15]/span")  
            post_season_year_dict['SO'] = strike_outs.text

            stolen_bases = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[16]/span")  
            post_season_year_dict['SB'] = stolen_bases.text

            batting_average = postseason_stats.find_element_by_xpath("//span[text()=" + current_year + "]//parent::td/parent::tr/td[18]/span")  
            post_season_year_dict['BA'] = batting_average.text
                        
        except NoSuchElementException as ex:
            print("No Post Season Stats for current year - Exception has been thrown. " + str(ex))
    
        try:
            ps_career_total = WebDriverWait(driver,  20).until(                                                                
                 EC.presence_of_element_located((By.XPATH, "//span[text()='MLB Career']//parent::td/parent::tr/td[5]/span" ))) 

            total_at_bats = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[5]/span")  
            post_season_career_dict['AB'] = total_at_bats.text

            total_runs = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[6]/span") 
            post_season_career_dict['R'] = total_runs.text

            total_hits = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[7]/span") 
            post_season_career_dict['H'] = total_hits.text

            total_homeruns = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[11]/span") 
            post_season_career_dict['HR'] = total_homeruns.text

            total_runs_batted_in = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[12]/span") 
            post_season_career_dict['RBI'] = total_runs_batted_in.text

            total_walks = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[13]/span") 
            post_season_career_dict['BB'] = total_walks.text

            total_strike_outs = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[15]/span")  
            post_season_career_dict['SO'] = total_strike_outs.text

            total_stolen_bases = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[16]/span")  
            post_season_career_dict['SB'] = total_stolen_bases.text

            total_batting_average = postseason_stats.find_element_by_xpath("//span[text()='MLB Career']//parent::td/parent::tr/td[18]/span")  
            post_season_career_dict['BA'] = total_batting_average.text

        except NoSuchElementException as ex:
            print("No Post Season Stats for career - Exception has been thrown. " + str(ex))
        
        end = datetime.now()
        duration = end - start
        print ("Total Time for Postseason Stats:")
        print (duration)
        
        return post_season_year_dict, post_season_career_dict

    
from tkinter import *
from PIL import ImageTk,Image
# https://pythonguides.com/python-tkinter-optionmenu/
root = Tk()
root.title("Player Stats")
root.geometry("800x800")

FrameIt=Frame(root)
FrameIt.grid(padx = 50, pady = 50)

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
    
     # ************* Season against pitcher and totals for career  *********************
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
    
    # ************* Post Season Stats for Year and Career  *********************
    batter_url = BP.getPlayerURL(g_selected_Batter, g_off_roster_list_of_dict)
    ps_year_stats_dict, ps_career_stats_dict = BP.getPostSeasonStats(batter_url)
    
    # Print current year postseason stats
    label_line = Label(FrameIt, text= "Postseason Stats(current year): ")
    label_line.grid(row=28, column=10, sticky='e')
    v_col = 10
    # print out stats to tkinter display
    for key in ps_year_stats_dict:
        label_line = Label(FrameIt, text= key + "\t")
        label_line.grid(row=29, column=v_col, sticky='e')
        label_line = Label(FrameIt, text= ps_year_stats_dict[key] + "\t")
        label_line.grid(row=30, column=v_col, sticky='e')
        v_col += 1
                       
    # Print career postseason stats
    label_line = Label(FrameIt, text= "Postseason Stats(career): ")
    label_line.grid(row=32, column=10, sticky='e')
    v_col = 10
    # print out stats to tkinter display
    for key in ps_career_stats_dict:
        label_line = Label(FrameIt, text= key + "\t")
        label_line.grid(row=33, column=v_col, sticky='e')
        label_line = Label(FrameIt, text= ps_career_stats_dict[key] + "\t")
        label_line.grid(row=34, column=v_col, sticky='e')
        v_col += 1
  
    # Post Season Stats
    print (ps_year_stats_dict)
    print (ps_career_stats_dict)

    
    
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
