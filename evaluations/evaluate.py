"""
VibeDine — Offline Evaluation Script
=====================================
Evaluates CF, CB, and Hybrid recommendation models using an 80/20 per-user
train/test split on the offline interaction data.

Run from the project root:
    py evaluate.py

Metrics reported: Precision@K, Recall@K, NDCG@K, Hit Rate@K  (K = 10, 20)
"""

import os
import pickle
import random
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

# ── Config ────────────────────────────────────────────────────────────────────

INTERACTIONS_FILE = "data/CF_interaction_matrix_1.parquet"
CBF_FEATURES_FILE = "data/CBF_item_features_1.parquet"
MODEL_CB_FILE     = "models/content_based_model.pkl"
MODEL_CF_FILE     = "models/item_cf_model.pkl"

MIN_RATING   = 4        # minimum rating to count as a positive interaction
TRAIN_RATIO  = 0.8      # 80% train, 20% test
MIN_INTERACTIONS = 5    # skip users with fewer interactions than this
N_EVAL_USERS = 1000     # cap on how many users to evaluate (speed)
K_VALUES     = [50, 100]
RANDOM_SEED  = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# ── Helpers ───────────────────────────────────────────────────────────────────

def precision_at_k(recommended, relevant, k):
    hits = len(set(recommended[:k]) & relevant)
    return hits / k

def recall_at_k(recommended, relevant, k):
    if not relevant:
        return 0.0
    hits = len(set(recommended[:k]) & relevant)
    return hits / len(relevant)

def ndcg_at_k(recommended, relevant, k):
    dcg = sum(
        1.0 / np.log2(rank + 2)
        for rank, item in enumerate(recommended[:k])
        if item in relevant
    )
    ideal_hits = min(len(relevant), k)
    idcg = sum(1.0 / np.log2(rank + 2) for rank in range(ideal_hits))
    return dcg / idcg if idcg > 0 else 0.0

def hit_rate_at_k(recommended, relevant, k):
    return 1.0 if set(recommended[:k]) & relevant else 0.0

def evaluate_recommendations(all_recs, test_sets, k_values):
    """
    all_recs  : dict[user_id -> list[gmap_id]] sorted by score descending
    test_sets : dict[user_id -> set[gmap_id]]
    """
    results = {k: {"precision": [], "recall": [], "ndcg": [], "hit_rate": []}
               for k in k_values}

    for user_id, relevant in test_sets.items():
        recs = all_recs.get(user_id, [])
        for k in k_values:
            results[k]["precision"].append(precision_at_k(recs, relevant, k))
            results[k]["recall"].append(recall_at_k(recs, relevant, k))
            results[k]["ndcg"].append(ndcg_at_k(recs, relevant, k))
            results[k]["hit_rate"].append(hit_rate_at_k(recs, relevant, k))

    return {
        k: {metric: np.mean(vals) for metric, vals in metrics.items()}
        for k, metrics in results.items()
    }

def print_results(name, results):
    print(f"\n{'─'*52}")
    print(f"  {name}")
    print(f"{'─'*52}")
    print(f"  {'K':>4}  {'Precision':>10}  {'Recall':>8}  {'NDCG':>8}  {'HitRate':>8}")
    print(f"{'─'*52}")
    for k, metrics in sorted(results.items()):
        print(
            f"  {k:>4}  "
            f"{metrics['precision']:>10.4f}  "
            f"{metrics['recall']:>8.4f}  "
            f"{metrics['ndcg']:>8.4f}  "
            f"{metrics['hit_rate']:>8.4f}"
        )
    print(f"{'─'*52}")

def get_alpha(n_train_likes):
    if n_train_likes <= 5:   return 0.0
    if n_train_likes <= 20:  return 0.4
    if n_train_likes <= 100: return 0.7
    return 0.85

def normalize(scores: dict) -> dict:
    if not scores:
        return {}
    vals = np.array(list(scores.values()), dtype=float)
    mn, mx = vals.min(), vals.max()
    if mx == mn:
        return {k: 0.5 for k in scores}
    return {k: float((v - mn) / (mx - mn)) for k, v in scores.items()}


# ── Step 1: Load and split data ───────────────────────────────────────────────

print("Loading interaction data...")
df = pd.read_parquet(INTERACTIONS_FILE)
df = df[df["rating"] >= MIN_RATING][["user_id", "gmap_id", "rating"]].copy()

# Keep users with enough interactions
counts = df.groupby("user_id").size()
valid_users = counts[counts >= MIN_INTERACTIONS].index.tolist()
df = df[df["user_id"].isin(valid_users)]

print(f"Users with ≥{MIN_INTERACTIONS} interactions: {len(valid_users):,}")

# Sample users for evaluation speed
eval_users = random.sample(valid_users, min(N_EVAL_USERS, len(valid_users)))
print(f"Evaluating on {len(eval_users):,} sampled users")

# Per-user 80/20 split
train_rows, test_sets = [], {}

for user_id, group in df.groupby("user_id"):
    rows = group.sample(frac=1, random_state=RANDOM_SEED)  # shuffle
    split = max(1, int(len(rows) * TRAIN_RATIO))
    train_rows.append(rows.iloc[:split])
    if user_id in set(eval_users):
        test_items = set(rows.iloc[split:]["gmap_id"].tolist())
        if test_items:
            test_sets[user_id] = test_items

train_df = pd.concat(train_rows, ignore_index=True)
print(f"Train interactions: {len(train_df):,} | Test users with held-out items: {len(test_sets):,}")


# ── Step 2: Build CF model from training data ─────────────────────────────────

print("\nBuilding CF model from training split...")

user_cat  = train_df["user_id"].astype("category")
item_cat  = train_df["gmap_id"].astype("category")

train_user_item = csr_matrix(
    (train_df["rating"].astype(float), (user_cat.cat.codes, item_cat.cat.codes))
)
train_item_user = train_user_item.T.tocsr()

user_id_to_idx  = dict(zip(user_cat.cat.categories, range(len(user_cat.cat.categories))))
item_id_to_idx  = dict(zip(item_cat.cat.categories, range(len(item_cat.cat.categories))))
idx_to_item_id  = dict(enumerate(item_cat.cat.categories))

print(f"CF matrix: {train_user_item.shape[0]:,} users × {train_user_item.shape[1]:,} items")


def cf_scores_for_user(user_id):
    if user_id not in user_id_to_idx:
        return {}
    uidx = user_id_to_idx[user_id]
    user_row = train_user_item[uidx]
    liked_indices = user_row.indices
    if len(liked_indices) == 0:
        return {}
    liked_ratings = user_row.data
    sims = cosine_similarity(train_item_user[liked_indices], train_item_user)
    for i, iidx in enumerate(liked_indices):
        sims[i, iidx] = 0
    numerator   = sims.T @ liked_ratings
    denominator = sims.sum(axis=0)
    scores = np.divide(numerator, denominator,
                       out=np.zeros_like(numerator, dtype=float),
                       where=denominator != 0)
    liked_set = set(liked_indices)
    return {idx_to_item_id[i]: float(scores[i])
            for i in range(len(scores)) if i not in liked_set}


# ── Step 3: Load CB model ─────────────────────────────────────────────────────

print("Loading CB model...")
with open(MODEL_CB_FILE, "rb") as f:
    cb_model = pickle.load(f)

cb_restaurants  = cb_model["restaurants"]          # DataFrame with gmap_id column
tfidf_matrix    = cb_model["tfidf_matrix"]
gmap_id_list    = cb_restaurants["gmap_id"].tolist()
gmap_id_to_cidx = {gid: i for i, gid in enumerate(gmap_id_list)}


def cb_scores_for_user(train_liked_ids):
    liked_indices = [gmap_id_to_cidx[g] for g in train_liked_ids if g in gmap_id_to_cidx]
    if not liked_indices:
        return {}
    user_scores = cosine_similarity(tfidf_matrix[liked_indices], tfidf_matrix).mean(axis=0)
    liked_set = set(train_liked_ids)
    return {gmap_id_list[i]: float(user_scores[i])
            for i in range(len(user_scores)) if gmap_id_list[i] not in liked_set}


# ── Step 4: Generate recommendations for all test users ───────────────────────

print(f"\nGenerating recommendations for {len(test_sets):,} test users...")

# Pre-build user → training likes map
user_train_likes = (
    train_df[train_df["user_id"].isin(test_sets)]
    .groupby("user_id")["gmap_id"]
    .apply(set)
    .to_dict()
)

cf_recs     = {}
cb_recs     = {}
hybrid_recs = {}

for i, user_id in enumerate(test_sets):
    if i % 100 == 0:
        print(f"  {i}/{len(test_sets)}", end="\r")

    train_liked = user_train_likes.get(user_id, set())
    n_likes     = len(train_liked)

    # CF
    cf_raw  = cf_scores_for_user(user_id)
    cf_norm = normalize(cf_raw)
    cf_recs[user_id] = sorted(cf_norm, key=cf_norm.get, reverse=True)

    # CB
    cb_raw  = cb_scores_for_user(train_liked)
    cb_norm = normalize(cb_raw)
    cb_recs[user_id] = sorted(cb_norm, key=cb_norm.get, reverse=True)

    # Hybrid
    alpha   = get_alpha(n_likes)
    all_ids = set(cf_norm) | set(cb_norm)
    hybrid  = {
        gid: alpha * cf_norm.get(gid, 0.0) + (1 - alpha) * cb_norm.get(gid, 0.0)
        for gid in all_ids
    }
    hybrid_recs[user_id] = sorted(hybrid, key=hybrid.get, reverse=True)

print(f"  Done.{' ' * 20}")


# ── Step 5: Compute and print metrics ─────────────────────────────────────────

print("\n" + "═"*52)
print("  EVALUATION RESULTS")
print("═"*52)

cf_results     = evaluate_recommendations(cf_recs, test_sets, K_VALUES)
cb_results     = evaluate_recommendations(cb_recs, test_sets, K_VALUES)
hybrid_results = evaluate_recommendations(hybrid_recs, test_sets, K_VALUES)

print_results("Collaborative Filtering (Item-Based CF)", cf_results)
print_results("Content-Based Filtering (TF-IDF)",       cb_results)
print_results("Hybrid (Adaptive Alpha)",                 hybrid_results)

print(f"\nEvaluated on {len(test_sets):,} users | "
      f"Train/Test split: {int(TRAIN_RATIO*100)}/{int((1-TRAIN_RATIO)*100)}\n")
