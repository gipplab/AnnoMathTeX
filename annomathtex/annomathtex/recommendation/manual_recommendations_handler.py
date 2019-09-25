import logging
from operator import itemgetter

from ..config import recommendations_limit

logging.basicConfig(level=logging.INFO)
manual_recommendations_handler_logger = logging.getLogger(__name__)

class ManualRecommendationsHandler:

    def __init__(self, existing_manual_recommendations):
        self.existing_manual_recommendations = existing_manual_recommendations


    def check_identifier_or_formula(self, symbol):


        manual_recommendations_handler_logger.info('Symbol: {}'.format(symbol))
        manual_recommendations_handler_logger.info('Existing manual recommendations: {}'.format(list(self.existing_manual_recommendations.keys())[0]))

        if symbol in self.existing_manual_recommendations:
            results = self.existing_manual_recommendations[symbol]
            sorted_results = sorted(results, key=itemgetter('count'), reverse=True)
            return sorted_results[:recommendations_limit]

        return []

