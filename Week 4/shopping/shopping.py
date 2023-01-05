import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    label = []
    months = {
        'Jan':1,
        'Feb':2,
        'Mar':3,
        'Apr':4,
        'May':5,
        'June':6,
        'Jul':7,
        'Aug':8,
        'Sep':9,
        'Oct':10,
        'Nov':11,
        'Dec':12
        }

    # Read data into file
    with open(filename, 'r') as fh:

        csv_reader = csv.reader(fh)
        header = next(csv_reader)   # Skip header
        temp = list(csv_reader)

        # Correct data
        for row in temp:
            # Add label value and remove label from list
            label_value = row.pop()
            label.append(1 if label_value == "TRUE" else 0)

            # Convert strings to int representations
            row[10] = months[row[10]]
            row[15] = 1 if row[15] == "Returning_Visitor" else 0
            row[16] = 1 if row[16] == "TRUE" else 0

            # Type cast elements in list
            dType = [int, float, int, float, int, float, float, float, float, float, int, int, int, int, int, int, int]
            evidence_temp = [t(x) for t,x in zip(dType, row)]
            evidence.append(evidence_temp)

    return evidence, label


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    pos_correct = 0
    neg_correct = 0
    pos_total = 0
    neg_total = 0
    for num in range(len(labels)):
        if labels[num] == 1:
            pos_total += 1
            if labels[num] == predictions[num]:
                pos_correct += 1
        else:
            neg_total += 1
            if labels[num] == predictions[num]:
                neg_correct += 1
    
    # Calculate proportions
    sensitivity = pos_correct / pos_total
    specificity = neg_correct / neg_total

    return sensitivity, specificity


if __name__ == "__main__":
    main()
