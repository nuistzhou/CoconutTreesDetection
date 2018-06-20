def fscore(recall, precision):
    return (2 * (recall * precision) / (precision + recall))