import numpy as np
class Player:
    def __init__(self,fname,lname,hasBall,currentZone,Team):
        self.fname = fname
        self.lname = lname
        self.hasBall = hasBall
        self.Index = currentZone
        self.Team = Team

    def move(self, FutureZone):
        self.currentZone = FutureZone

    def get_currentZone(self):
        return self.currentZone
    def get_pass_success(self, passing, target_zone):
        
        zones_away = self.get_zones_away(target_zone)
        dfp_arnd = self.check_dfp_arnd_target()
        dfp_in = self.check_dfp_in_target()

        if dfp_arnd == False:
                
            denominator = 1 + np.exp((-0.25 * passing) + (0.25 * zones_away) + (0.6 * dfp_in))
        else:
            ant_attr = "1." + str()
            
            denominator = 1 + np.exp(((-0.25 * passing) + (0.25 * zones_away) + (0.6 * dfp_in))/float(ant_attr))
        return 1/(denominator)

    def get_zones_away(self,target_zone):
        pass

    def check_dfp_arnd_target(self):
        pass


