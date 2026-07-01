import unittest
from unittest.mock import patch

from api.services.recommendation_service import get_hybrid_recommendations_for_user


class RecommendationServiceColdStartTests(unittest.TestCase):
    @patch("api.services.recommendation_service.get_popular_restaurants", return_value=[{"gmap_id": "abc"}])
    @patch("api.services.recommendation_service.extract_gmap_ids", return_value=["abc"])
    @patch("api.services.recommendation_service.get_filtered_restaurants_repo", return_value=[{"gmap_id": "abc"}])
    @patch("api.services.recommendation_service.get_onboarding_preferences", return_value={"preferences": {"favorite_categories": [], "favorite_atmospheres": [], "accessibility": [], "dietary_restrictions": []}})
    @patch("api.services.recommendation_service.get_user_augmented_likes", return_value=0)
    def test_hybrid_recommendations_reuse_precomputed_onboarding_candidates(
        self,
        mock_augmented_likes,
        mock_onboarding_preferences,
        mock_filtered_restaurants_repo,
        mock_extract_gmap_ids,
        mock_get_popular_restaurants,
    ):
        results = get_hybrid_recommendations_for_user(
            "user-1",
            top_k=1,
            onboarding_candidate_gmap_ids=["abc"],
        )

        self.assertEqual(results[0]["gmap_id"], "abc")
        mock_onboarding_preferences.assert_not_called()
        mock_filtered_restaurants_repo.assert_not_called()
        mock_extract_gmap_ids.assert_not_called()


if __name__ == "__main__":
    unittest.main()
