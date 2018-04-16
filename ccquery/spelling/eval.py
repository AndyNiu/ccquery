import logging
from ccquery.error import DataError
from ccquery.utils import io_utils
from ccquery.data import json_controller

class Evaluation:
    """
    Evaluate the performance of the automatic spelling correction

    Consider the case of
    - |Q| input queries
    - each query q has multiple candidate corrections
        algorithm suggests more than 1 correction
        C(q) = the list of candidate corrections for query q
    - each query q has multiple valid corrections
        the query can be correctly spelled in more than 1 way
        G(q) = the list of gold, real corrections for query q

    Use the following evaluation metrics
    - recall@N evaluate the performance of correction
        the number of correct suggestions in the top ranked N sugestions
            divided by the total number of suggestions in the ground truth
        R@N = 1 / |Q| * sum( |C(q) ∩ G(q)| / |G(q)| )
    - precision@N evaluate the quality of suggestions
        the number of correct suggestions in the top ranked N sugestions
          divided by the smaller value of N or the total number of suggestions
        P@N = 1 / |Q| * sum( |C(q) ∩ G(q)| / min(N, |C(q)|) )
    - F1@N = (2 * P@N * R@N) / (P@N + R@N)

    Use case
    -----------
    Consider
    - |Q| = 300 user queries
    -  50 queries should be modified (they contain spelling errors)
    - 250 queries should not be modified (they do not contain any errors)
    - only one gold correction for each query
    - a 'do nothing' algorithm: each input query is left intact

    The performance of the 'do nothing' algorithm is then
    - R@1 = 1 / 300 * ( 50 * 0 + 250 * 1) = 83.33%
    - P@1 = 1 / 300 * ( 50 * 0 + 250 * 1) = 83.33%
    - F1@1 = 83.33%
    """

    def __init__(self):
        """Initialize the pergormance evaluation"""
        self.data = None
        self.logger = logging.getLogger(__name__)

    def load_from_file(self, path, candidate='suggestion', gold='clean',):
        """Load data from jsonl file"""
        io_utils.check_file_readable(path)
        self.data = json_controller.stream(path, candidate, gold)

    def load_from_list(self, data):
        """Load data from existing list"""
        self.data = iter(data)

    def load_from_lists(self, candidate_list, gold_list):
        """Load data from existing lists"""
        self.data = iter(zip(candidate_list, gold_list))

    def performance(self, n=5):
        """Evaluate the R@N, P@N, F1@N performance of current suggestions"""

        recall_n = 0
        precision_n = 0

        n_queries = 0
        for suggestions, corrections in self.data:
            n_queries += 1

            if not isinstance(suggestions, list):
                suggestions = [suggestions]
            if not isinstance(corrections, list):
                corrections = [corrections]

            # keep at most top N suggestions
            suggestions = suggestions[:n]

            n_suggestions = len(suggestions)
            n_corrections = len(corrections)

            # intersection between suggestions list and gold-corrections list
            n_correct = 0
            for gold in corrections:
                if gold in suggestions:
                    n_correct += 1

            if n_suggestions < n:
                divp = n_suggestions
            else:
                divp = n

            recall_n += n_correct / n_corrections
            precision_n += n_correct / divp

        if n_queries == 0:
            raise DataError('No corrections available for evaluation')

        recall_n = round(recall_n / n_queries * 100, 2)
        precision_n = round(precision_n / n_queries * 100, 2)
        f1_n = round((2 * recall_n * precision_n) / (recall_n + precision_n), 2)

        self.logger.info("R@N={}\nP@N={}\nF1@N={}".format(
            recall_n, precision_n, f1_n))

        return recall_n, precision_n, f1_n
