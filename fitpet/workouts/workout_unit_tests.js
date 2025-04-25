

test('should create an exercise', () => {
    const ex = new Exercise(1, "pushup", 2, 30, 1);
    expect(ex.id).toBe(1);
    expect(ex.name).toBe("pushup");
    expect(ex.level).toBe(2);
    expect(ex.maxReps).toBe(30);
    expect(ex.tiers).toBe(1);
  });

test('tiers can only be 1-3', () => {
    const ex = new Exercise(1, "pushup", 0, 20, 1);
    expect(ex.level).toBe(1);
    expect(() => {
        new Exercise(1, "pushup", 5, 20, 4);
      }).toThrow("Level must be between 1 and 3");
  });

test('typechecking', () => {
    new Exercise('a', "pushup", 5, 20, 4);
      }).toThrow("ID must be positive int");
test('typechecking', () => {
    new Exercise(1, 3, 5, 20, 4);
      }).toThrow("name must be string");
test('typechecking', () => {    new Exercise(1, "pushup", 0.5, 20, 4);
        }).toThrow("level must be positive int");
test('typechecking', () => {new Exercise(1, "pushup", 1, 0.5, 4);
    }).toThrow("reps must be positive int");
test('typechecking', () => {new Exercise(1, "pushup", 1, 20, 'a');
        }).toThrow("tier must be positive int");
test('typechecking', () => {new Exercise(1, "pushup", 1, -1, 4);
    }).toThrow("reps must be positive int");

test('xp calculation', () => {
    const ex = new Exercise(1, "pushup", 2, 30, 1);
    // Formula MIGHT BE CHANGED but for now its reps*tier*level
    expect(ex.calculateXP(10)).toBe(20);
  });

test('coin calculation', () => {
    const ex = new Exercise(1, "pushup", 2, 30, 1);
    // Formula MIGHT BE CHANGED but for now its reps*tier*level
    expect(ex.calculateCoins(10)).toBe(20)
  });

test('not exceeding max reps', () => {
    log_ex(pushups,1,3000000).toThrow("exceeded reps");
  });

//tests for the diagram arrows lowkeys

test('start an excersise', () => {
    Exercise(1, "pushup", 2, 30, 1);
  });
test('give up workout', () => {
    //unclear for now
  });
test('give up exersise', () => {
    //unclear for now
    //go back to the exersise menu
  });
test('earn coins and xp', () => {
    //set_user to have 50 coins
    Exercise(1, "pushup", 2, 30, 1);
    expect(User.getcoins()).toBe(70);
    expect(User.getxp()).toBe(70);
  });
  test('levelup', () => {
    //set_user(close to levelling up to 2)
    Exercise(1, "pushup", 2, 30, 1);
    expect(User.getlevel()).toBe(2);
  });
