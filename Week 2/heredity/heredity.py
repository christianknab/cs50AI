import csv
import itertools
from logging import raiseExceptions
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Initialize probability variable
    probability = 1
    
    # Loop through every person in people dictionary
    for person in people:

        # Set what we need to check
        gene_num = 1 if person in one_gene else 2 if person in two_genes else 0
        has_trait = True if person in have_trait else False

        # Set to gene and trait distribution
        gene_probability = PROBS["gene"][gene_num]
        trait_probability = PROBS["trait"][gene_num][has_trait]

        # No parents listed
        if people[person]["mother"] is None and people[person]["father"] is None:

            probability = probability * gene_probability * trait_probability

        else:

            # Find person's parents
            mother_name = people[person]["mother"]
            father_name = people[person]["father"]

            # Set parent's probabiltiy of passing gene to child
            mother_gives_trait_prob = 0.5 if mother_name in one_gene else 1 - PROBS['mutation'] if mother_name in two_genes else PROBS['mutation']
            father_gives_trait_prob = 0.5 if father_name in one_gene else 1 - PROBS['mutation'] if father_name in two_genes else PROBS['mutation']

            # Probability of one gene given
            if gene_num == 1:
        
                # Probability either mother gives and father doesn't and vice versa
                probability *= (1 - mother_gives_trait_prob) * father_gives_trait_prob + (1 - father_gives_trait_prob) * mother_gives_trait_prob
            
            # Probability of two genes given
            elif gene_num == 2:

                # Probability both mother and father gives gene
                probability *= mother_gives_trait_prob * father_gives_trait_prob

            # Probability no copies given
            elif gene_num == 0:

                # Probability neither mother nor father gives a gene
                probability *= (1 - mother_gives_trait_prob) * (1 - father_gives_trait_prob)

            else:
                raise ValueError

            # Multiply probability by the probability that the trait is actually present
            probability *= trait_probability

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # Loop through every person
    for person in probabilities:
        # Initialize gene and traits
        gene_num = 1 if person in one_gene else 2 if person in two_genes else 0
        has_trait = True if person in have_trait else False
        
        # Add the probabilties to dictionary
        probabilities[person]["gene"][gene_num] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # Loop through every person
    for person in probabilities:
        # Initialize variables
        gene_sum = 0
        trait_sum = 0

        # Adjust gene probabilities
        for gene_num in range(0, 3):
            gene_sum += probabilities[person]["gene"][gene_num]
        
        # Normalize gene
        norm_value = 1 / gene_sum
        for gene_num in range(0, 3):
            probabilities[person]["gene"][gene_num] *= norm_value

        # Adjust trait probabilities
        trait_sum += probabilities[person]["trait"][True]
        trait_sum += probabilities[person]["trait"][False]

        # Normalize trait
        norm_value = 1 / trait_sum
        probabilities[person]["trait"][True] *= norm_value
        probabilities[person]["trait"][False] *= norm_value


if __name__ == "__main__":
    main()
