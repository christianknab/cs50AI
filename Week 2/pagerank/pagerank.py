import os
import random
import re
import sys
from tkinter import N

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # corpus = crawl("corpus0")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Initialize empty dictionary
    page_rank = {}
    corpus_length = len(corpus)
    links_length = len(corpus[page])

    # If there are no links in current file,
    # return equal probability for every page
    equal_probability = (1 / corpus_length)

    if corpus[page] == "":
        for key in corpus:
            page_rank[key] = equal_probability
        return page_rank

    # Each page gets (1 - damping_factor) / n as initial probability
    initial_probability = ((1 - damping_factor) / corpus_length)
    added_probability = (damping_factor / links_length)

    for key in corpus:
        if key not in corpus[page]:
            page_rank[key] = initial_probability

        # Each page gets (damping_factor / n - 1) added
        else:
            page_rank[key] = initial_probability + added_probability
    
    return(page_rank)


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create a copy of the pages with 0 values
    corpus_copy = corpus.copy()
    for page in corpus_copy:
        corpus_copy[page] = 0

    # Initialize variables
    random_index = random.randint(0, (len(corpus) - 1))
    chosen_page = list(corpus.keys())[random_index]

    # Create n number of samples
    for _ in range(n):
    
        # Get probability distribution of the sample
        probability = transition_model(corpus, chosen_page, damping_factor)
        probability_keys = list(probability.keys())
        probability_weights = [probability[i] for i in probability]
        chosen_page = random.choices(probability_keys, probability_weights, k=1)[0]

        # Keep track of how many times a certain page is picked
        corpus_copy[chosen_page] += 1
    
    # Divide by n to find individual page probabilities
    for page in corpus_copy:
        corpus_copy[page] /= n

    return corpus_copy


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize dictionaries
    new_probs = {}
    old_probs = {}

    corpus_length = len(corpus)

    # First condition in equation
    first_condition = (1 - damping_factor) / corpus_length

    # Initial probabilities
    for page in corpus:
        old_probs[page] = 1 / corpus_length

    # Adding second condition in equation
    while True:

        # Check if current page is linked in another page
        for page in corpus:
            second_condition = 0
            for link_page in corpus:

                # If another page is linked to the current page
                # add second condition
                if page in corpus[link_page]:
                    num_links = len(corpus[link_page])
                    second_condition += old_probs[link_page] / num_links
                # If a page has no links at all
                # interpret every other page as having the same chance of being clicked
                if len(corpus[link_page]) == 0:
                    second_condition += old_probs[link_page] / corpus_length

            # Sum conditions and add to dictionary
            second_condition = damping_factor * second_condition + first_condition
            new_probs[page] = second_condition

        # Check if done calculating probabilities
        difference = max([abs(new_probs[x] - old_probs[x]) for x in old_probs])

        if difference < 0.001:
            break
        else:
            old_probs = new_probs.copy()

    return new_probs


if __name__ == "__main__":
    main()
