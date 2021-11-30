import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


class Champion():
    def __init__(self, champ_name = '', champ_role = '', champ_wr = 0.0, champ_rr = 0.0, champ_pr = 0.0, champ_br = 0.0, champ_presence = 0.0, champ_kda = 0.0):
        self.cname = champ_name
        self.crole = champ_role
        self.cwr = champ_wr
        self.crr = champ_rr
        self.cpr = champ_pr
        self.cbr = champ_br
        self.cpresence = round(champ_presence, 2)
        self.ckda = champ_kda
    def get_name(self): 
        return self.cname
    def get_role(self):
        return self.crole
    def get_winrate(self):
        return self.cwr
    def get_rolerate(self):
        return self.crr
    def get_pickrate(self):
        return self.cpr
    def get_banrate(self):
        return self.cbr
    def get_presence(self):
        return self.cpresence
    def get_kda(self):
        return self.ckda  
    def get_champion(self):
        return "{} {} {}% {}% {}% {}% {}% {}".format(self.cname, self.crole, self.cwr, self.crr, self.cpr, self.cbr, self.cpresence,self.ckda)
class Role():
    def __init__(self, role_champs):
        self.champions_in_role = role_champs
        self.role_wr = [rchamp.get_winrate() for rchamp in role_champs]
        self.role_rr = [rchamp.get_rolerate() for rchamp in role_champs]
        self.role_pr = [rchamp.get_pickrate() for rchamp in role_champs]
        self.role_br = [rchamp.get_banrate() for rchamp in role_champs]
        self.role_pres = [rchamp.get_presence() for rchamp in role_champs]
        self.role_kda = [rchamp.get_kda() for rchamp in role_champs]   
    def get_role_wr(self):
        return self.role_wr
    def get_role_rr(self):
        return self.role_rr
    def get_role_pr(self):
        return self.role_pr
    def get_role_br(self):
        return self.role_br
    def get_role_pres(self):
        return self.role_pres
    def get_role_kda(self):
        return self.role_kda
     
with open('champion_stats.txt') as champion_stats_txt:

    raw_champion_data = champion_stats_txt.readlines()
    champs = []
    roles = []
    winrate = []
    rolerate = []
    pickrate = []
    banrate = []
    presence = []
    kda = []
    
    #This methods fills the lists of champion information by stripping the file of of \n and splitting by spaces
    #Only the last 5 entres are needed when taking in statistics such as winrate and rolerate because we are 
    #Discarding the first 4 entries on the line (tier, letter grade) because they are very subjective
    def make_lists(thresh):
    
        for i in range(0, len(raw_champion_data), 3):
            if float(raw_champion_data[i + 2].strip('\n').split()[-4][:-1]) > thresh: 
                champs.append(raw_champion_data[i].strip('\n').split(',')[0].strip('\"'))
                roles.append(raw_champion_data[i + 1].strip('\n'))
                winrate.append(float(raw_champion_data[i + 2].strip('\n').split()[-5:][0][:-1]))
                rolerate.append(float(raw_champion_data[i + 2].strip('\n').split()[-5:][1][:-1]))
                pickrate.append(float(raw_champion_data[i + 2].strip('\n').split()[-5:][2][:-1]))
                banrate.append(float(raw_champion_data[i + 2].strip('\n').split()[-5:][3][:-1]))
                presence.append(float(pickrate[-1] + banrate[-1]))
                kda.append(float(raw_champion_data[i + 2].strip('\n').split()[-5:][4]))

    def printAllChampStats(champ_list): 
        
        for cham in champ_list:
            print(cham.get_champion())
        print("\nFormatted as: Champion ROLE Win% Role% Pick% Ban% KDA\n\n")
    
    def create_champs():
        champions_list = []
        for i in range(len(champs)):
            cham = Champion(champ_name=champs[i], champ_role=roles[i], champ_wr=float(winrate[i]), champ_rr=float(rolerate[i]), champ_pr=float(pickrate[i]), champ_br=float(banrate[i]), champ_presence=float(presence[i]), champ_kda=float(kda[i]))
            champions_list.append(cham)
        return champions_list

    def compile_role(champ_list, desired_role) :
        champs_in_role = []
        for character in champ_list:
            if character.get_role() == desired_role:
                champs_in_role.append(character)
        return champs_in_role

    def draw_graph(listx, listy, xname, yname):
            listx = np.array(listx)
            listy = np.array(listy)
            plt.xlabel(xname)
            plt.ylabel(yname)
            plt.title(xname + " vs. " + yname + "\nin League of Legends")
            xlist = listx.reshape(-1, 1)
            ylist = listy.reshape(-1, 1)
            plt.scatter(listx, listy, s = 1)
            linear_regressor = LinearRegression()
            linear_regressor.fit(xlist, ylist)
            r2 = round(linear_regressor.score(xlist, ylist), 5)
            y_predictions = linear_regressor.predict(xlist)
            plt.plot(xlist, y_predictions, color = 'red')
            plt.text(max(xlist), min(y_predictions), "R$^2$ = {}".format(r2))        
            plt.show()

    def create_dict(role_list):
        return {"W": ["Win rate (%)", role_list.get_role_wr()], "R":["Role rate (%)", role_list.get_role_rr()], 
    "P": ["Pick rate (%)", role_list.get_role_pr()], "B":["Ban rate (%)", role_list.get_role_br() ], "K": ["KDA", role_list.get_role_kda()], "PR": ["Presence (%)", role_list.get_role_pres()]}    

    def get_variable():
        correct = ["W", "R", "P", "B", "K", "PR"]
        i = 0
        while True:
            if i > 0:
                print("\nInvalid value. Please try again.")
            userstat = input("\nEnter one of the following as a Variable (Not case-sensitive):\n'W' for Win rate\n'R' for Role rate\n'P' for Pick rate\n'B' for Ban rate\n'K' for KDA\n'PR' for Presence\n").upper()
            i += 1
            if userstat in correct:
                break
        return userstat


    print("\nWelcome to the League of Legends Champion Stat Project!")

    make_lists(float(input("""\nEnter lower threshold for pick rate in role to discard very rare picks in certain roles
(This will get rid of low playrate duplicates).
Enter '0' to keep all values:\n""")))
    
    list_of_champions = create_champs()
    top_laners = Role(compile_role(list_of_champions, "TOP"))
    junglers = Role(compile_role(list_of_champions, "JUNGLE"))
    mid_laners = Role(compile_role(list_of_champions, "MID"))
    adcs = Role(compile_role(list_of_champions, "ADC"))
    supports = Role(compile_role(list_of_champions, "SUPPORT"))
    print("TOP LANERS:\n")
    printAllChampStats(top_laners.champions_in_role)
    print("JUNGLERS:\n")
    printAllChampStats(junglers.champions_in_role)
    print("MID LANERS:\n")
    printAllChampStats(mid_laners.champions_in_role)
    print("ADCS:\n")
    printAllChampStats(adcs.champions_in_role)
    print("SUPPORTS:\n")
    printAllChampStats(supports.champions_in_role)
    input_dict = {"T": top_laners, "J": junglers, "M": mid_laners, "A": adcs, "S": supports}
    while True:
        role_selection = input("What role would you like to compare stats for?\nT for Top\nJ for Jungle\nM for Mid\nA for ADC\nS for Support\n").upper()
        if(role_selection in input_dict):
            break
        print("Invalid entry. Try again.")

    role_to_graph = create_dict(input_dict[role_selection])

    print("\n\n\nPlease select an Independent Variable")
    varx = get_variable()

    print("\n\nGreat, now for the Dependent Variable")
    vary = get_variable()

    draw_graph(role_to_graph[varx][1], role_to_graph[vary][1], role_to_graph[varx][0], role_to_graph[vary][0])
