#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!/usr/bin/env python
# coding: utf-8

from Stat_Query import *

# The variable division needs to be set to the one to review.
# American League West = regularSeason-division-200
# American League East = regularSeason-division-201
# American League Central = regularSeason-division-202
# National League West = regularSeason-division-203 
# National League East = regularSeason-division-204
# National League Central = regularSeason-division-205
      
division = "regularSeason-division-203" # NL West
# Stat Query Class - all Selenium related calls.
SQ = Stat_Query(division)

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

# ********************************* Retrieve Record ****************************************************
def retrieve_record():
    
    current_records_dict = {}

    current_records_dict = {}        
    current_records_dict = SQ.getCurrentRecords()

    return current_records_dict
# ********************************* Games Remaining *****************************************************              
def games_remaining(wins, losses):
    
    games_played = wins + losses
    games_remain = 162 - games_played
    
    return games_remain

# ********************************* Calcuate Winning Percentage *****************************************
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

# ********************************* Trailing Team *******************************************************
def trailing_team(win_list_of_dict, team_name, wins, losses):
    
    dict_trail_team_results = {}
    trailing_list_of_dict = []
    for win_dict in win_list_of_dict:
        for key, value in win_dict.items():
            if isinstance(value, dict):
                for winlossrec in value.items():
                    if key == "Final_Record":
                        trail_wins = int(winlossrec[0]) - wins
                        trail_losses = int(winlossrec[1]) - losses
                        trail_final_wins = wins + trail_wins
                        trail_final_losses = losses + trail_losses
                        
                        final_record = "Final_Record"
                        dict_trail_team_results = {team_name: 
                                                     {str(round(trail_wins )): str(round(trail_losses ))}, 
                                                    final_record:  
                                                     {str(round(trail_final_wins)): str(round(trail_final_losses))}
                                                    }
                        trailing_list_of_dict.append(dict_trail_team_results)
   
       
    return  trailing_list_of_dict

# ********************************* Over and Under Calculation Tally ***************************************
def over_under_calc_tally(opponent_win_loss_list_of_dict, opponent_team_dict):
    
    gamesOver500 = 0
    for dict_record in opponent_win_loss_list_of_dict:
        for key,value in dict_record.items():
            for wl in value.items():
                over500 = int(wl[0]) - int(wl[1])
                
                if over500 > 0:
                    if key in opponent_team_dict.keys():
                        gamesOver500 = gamesOver500 + int(opponent_team_dict[key])
    
    return(gamesOver500)
                

# ********************************* Get Opponent Information **********************************************
def get_opponent_info(teamInfoURL):

    gameDates = []
    gameDates = SQ.getScheduleDates(teamInfoURL)
    
    opponent_team_dict = {}
    opponent_team_dict = SQ.getTeamNameAndCountOfGamesRemaining(teamInfoURL, gameDates)
    
    opponent_win_loss_list_of_dict = []
    opponent_win_loss_list_of_dict = SQ.getWinLossRecordForOpponent(opponent_team_dict)
    
    gamesOver500 = over_under_calc_tally(opponent_win_loss_list_of_dict, opponent_team_dict)
    return (gamesOver500,  opponent_win_loss_list_of_dict, opponent_team_dict)
    

    # ********************************* Over and Under Calculation ****************************************
def over_under_calc():
   
    URL_Schedule_List = []
    URL_Schedule_List = SQ.getScheduleURL()

    g_wt_href = URL_Schedule_List[0]  # winning team url link for reporting
    w_gamesOver500,  w_opponent_win_loss_list_of_dict, w_opponent_team_dict = get_opponent_info(URL_Schedule_List[0])            

    g_tt_href = URL_Schedule_List[1]  # trailing team url link for reporting
    t_gamesOver500,  t_opponent_win_loss_list_of_dict, t_opponent_team_dict = get_opponent_info(URL_Schedule_List[1])            

                
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
    
# ********************************* Calcuate Winning Percentage ******************************************
def calc_winning_percentage(wins,losses):
    total = float(wins) + float(losses)
    win_percentage = float(wins)/float(total)
    return win_percentage

def format_win_perc(win_perc):
    
    wp = str(win_perc)
    wp = wp[1:5]
    wp = wp.ljust(4, '0')
    return wp
                    
# # ********************************* Print Team Results *************************************************
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

# *********************************Main **************************************************************
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

print ()
print ("\t\t\t\t", "end of report")

