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

    @patch("api.services.recommendation_service.compute_cb_scores", return_value={"abc": 1.0})
    @patch("api.services.recommendation_service.compute_cf_scores", return_value={"abc": 0.5})
    @patch("api.services.recommendation_service.get_user_alpha", return_value=0.5)
    def test_get_hybrid_scores_for_user_computes_once_per_request(
        self,
        mock_get_user_alpha,
        mock_compute_cf_scores,
        mock_compute_cb_scores,
    ):
        from api.services.recommendation_service import get_hybrid_scores_for_user

        hybrid_scores = get_hybrid_scores_for_user("user-2")

        self.assertEqual(hybrid_scores["abc"], 0.75)
        mock_compute_cb_scores.assert_called_once_with("user-2")
        mock_compute_cf_scores.assert_called_once_with("user-2")
        mock_get_user_alpha.assert_called_once_with("user-2")


if __name__ == "__main__":
    unittest.main()
