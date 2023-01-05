from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Implication(AKnight, And(AKnight, AKnave)),         # If A is a Knight, A is both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave))),     # If A is a Knave, A is not both a knight and a knave
    Not(And(AKnight, BKnave)),                          # One cannot be both a knight and a knave
    Or(AKnight, AKnave)                                 # One is either a knight or a knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Not(And(AKnight, AKnave)),                          # One cannot be both a knight and a knave
    Not(And(BKnight, BKnave)),                          
    Or(AKnight, AKnave),                                # One is either a knight or a knave
    Or(BKnight, BKnave),

    Implication(AKnight, And(AKnave, BKnave)),          # If A is a knight, A and B are both knaves
    Implication(AKnave, Not(And(AKnave, BKnave)))       # If A is a knave, A and B can't both be knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Not(And(AKnight, AKnave)),                          # One cannot be both a knight and a knave
    Not(And(BKnight, BKnave)),                          
    Or(AKnight, AKnave),                                # One is either a knight or a knave
    Or(BKnight, BKnave),

    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),           # If A is a knight, they are both a knight or both a knave
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),       # If A is a knave, they are not both a knight or a knave
    Implication(BKnave, Or(And(AKnave, BKnave), And(AKnight, BKnight))),            # If B is a knave, they are not different
    Implication(BKnight, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight))))       # If B is a knight, they are both different
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Not(And(AKnight, AKnave)),                          # One cannot be both a knight and a knave
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    Or(AKnight, AKnave),                                # One is either a knight or a knave
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),

    # A is either
    Or(
        # If A says "I am a knight"
        And(
            Implication(AKnight, AKnight),              # If A actually is a knight, then he is a knight
            Implication(AKnave, Not(AKnight))           # If A is actually a knave, then he is not a knight
        ),
        # If A says "I am a knave"
        And(
            Implication(AKnight, AKnave),               # If A is actually a knight, then he is a knave
            Implication(AKnave, Not(AKnave))            # If A is actually a knave, then he is not a knave
        )
    ),

    # But A cannot be both
    Not(And(
        # If A says "I am a knight"
        And(
            Implication(AKnight, AKnight),              # If A actually is a knight, then he is a knight
            Implication(AKnave, Not(AKnight))           # If A is actually a knave, then he is not a knight
        ),
        # If A says "I am a knave"
        And(
            Implication(AKnight, AKnave),               # If A is actually a knight, then he is a knave
            Implication(AKnave, Not(AKnave))            # If A is actually a knave, then he is not a knave
        )
    )),

    # B says "A said 'I am a knave'."
    Implication(BKnight, And(                           # If B is a knight, then:
            Implication(AKnight, AKnave),                   # If A is actually a knight, then he is a knave
            Implication(AKnave, Not(AKnave))                # If A is actually a knave, then he is not a knave
    )),

    Implication(BKnave, And(                            # If B is a knave, then:
            Implication(AKnight, AKnight),                  # If A actually is a knight, then he is a knight
            Implication(AKnave, Not(AKnight))               # If A is actually a knave, then he is not a knight
    )),

    # B says "C is a knave."
    Implication(BKnight, CKnave),                       # If B is a knight, then C is a knave
    Implication(BKnave, CKnight),                       # If B is a knave, then C is a knight

    # C says "A is a knight."
    Implication(CKnight, AKnight),                      # If C is a knight, then A is a knight
    Implication(CKnave, AKnave)                         # If C is a knave, then A is a knave
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
