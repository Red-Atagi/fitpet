from signals import populate_static_models


class Exercise:
    """     constructor(name, maxReps, tier) {      
      this.name = name;          
      this.maxReps = maxReps; 
      this.tier = tier;     
    } """
   
    def __init__ (name, maxreps, tier, self):
      self.name = name 
      self.maxreps = maxreps
      self.tier = tier
    

    def calculateXP(reps , level, self):
      #dont know the formula yet
      if (self.maxReps > reps):
        return self.tier * reps * level
      else:
        return self.tier * self.maxReps * level
    
  
    def calculateCoins(reps, level, self):
      #dont know the formula yet
      if (self.maxReps > reps):
        return self.tier * reps * level
      else:
        return self.tier * self.maxReps * level

    #check if user is ready to level up
    #dont know yet what the level thresholds are but Im gonna assume every 1000
    #we need to make sure you cant go 2 levels up? can we meet with the user ppl to talk about it maybe
    def is_level_up(level, currentxp, extraxp):
        if ((currentxp + extraxp)%1000 < level):
            return False
        else:
            return True
        
    def changeExercise():
        return -1

    def abortExercise():
        return -1

    def runExerciseMenu():
        while True:    
            #select an exercise - select from a menu
            #start to exercise - go to the log screen
            '''
            if (aborts):
                return

            if (changes exercise)
                continue

            if submits workout
                coins = calculateCoins(reps, level)
                extraXP = calculateXP(reps,level)
                self.fpuser.addCoins(coins)
                self.fpuser.save()
                if (is_level_up(level, currentxp, extraxp))
                    levelup()
                self.fpuser.addXP(extraXP)
                self.fpuser.save()
            '''



