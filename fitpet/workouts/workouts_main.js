class Exercise {
    constructor(id, name, level, maxReps, tiers) {
      this.id = id;          
      this.name = name;      
      this.level = level;    
      this.maxReps = maxReps; 
      this.tiers = tiers;     
    }
  
    calculateXP(reps) {
      //dont know the formula yet
      return this.tiers * reps * this.level;
    }
  
    calculateCoins(reps) {
      //dont know the formula yet
     return this.tiers * reps * this.level;
    }
    //get

    //set
    
    
  }
