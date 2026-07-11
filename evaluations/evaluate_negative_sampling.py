"""
VibeDine — Negative Sampling Evaluation
========================================
For each held-out test interaction, sample 99 random negative restaurants
(items the user has never interacted with). The model ranks all 100 candidates
(1 positive + 99 negatives) and we check if the positive item appears in top-K.

This mirrors the standard protocol used in RecSys academic papers and gives
much more interpretable metrics than full-catalog ranking.

Run from the project root:
    py evaluate_negative_sampling.py

Metrics: Hit Rate@K, NDCG@K  (K = 1, 5, 10, 20)
"""

import pickle
import random
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

# ── Config ────────────────────────────────────────────────────────────────────

INTERACTIONS_FILE = "data/CF_interaction_matrix_1.parquet"
MODEL_CB_FILE     = "models/content_based_model.pkl"
MODEL_CF_FILE     = "models/item_cf_model.pkl"

MIN_RATING       = 4
MIN_INTERACTIONS = 5
N_EVAL_USERS     = 1000
N_NEGATIVES      = 99     # negatives per test item → 100 candidates total
K_VALUES         = [1, 5, 10, 20]
RANDOM_SEED      = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# ── Metrics ───────────────────────────────────────────────────────────────────

def hit_rate_at_k(ranked, positive, k):
    return 1.0 if positive in ranked[:k] else 0.0

def ndcg_at_k(ranked, positive, k):
    if positive not in ranked[:k]:
        return 0.0
    rank = ranked.index(positive)
    return 1.0 / np.log2(rank + 2)

def evaluate(all_results, k_values):
    out = {k: {"hit_rate": [], "ndcg": []} for k in k_values}
    for ranked, positive in all_results:
        for k in k_values:
            out[k]["hit_rate"].append(hit_rate_at_k(ranked, positive, k))
            out[k]["ndcg"].append(ndcg_at_k(ranked, positive, k))
    return {k: {m: np.mean(v) for m, v in metrics.items()} for k, metrics in out.items()}

def print_results(name, results):
    print(f"\n{'─'*46}")
    print(f"  {name}")
    print(f"{'─'*46}")
    print(f"  {'K':>4}  {'Hit Rate':>10}  {'NDCG':>10}")
    print(f"{'─'*46}")
    for k, metrics in sorted(results.items()):
        print(f"  {k:>4}  {metrics['hit_rate']:>10.4f}  {metrics['ndcg']:>10.4f}")
    print(f"{'─'*46}")

def get_alpha(n):
    if n <= 5:   return 0.0
    if n <= 20:  return 0.4
    if n <= 100: return 0.7
    return 0.85

def normalize(scores):
    if not scores:
        return {}
    vals = np.array(list(scores.values()), dtype=float)
    mn, mx = vals.min(), vals.max()
    if mx == mn:
        return {k: 0.5 for k in scores}
    return {k: float((v - mn) / (mx - mn)) for k, v in scores.items()}

# ── Load & Split ──────────────────────────────────────────────────────────────

print("Loading interaction data...")
df = pd.read_parquet(INTERACTIONS_FILE)
df = df[df["rating"] >= MIN_RATING][["user_id", "gmap_id", "rating"]].copy()

counts = df.groupby("user_id").size()
valid_users = counts[counts >= MIN_INTERACTIONS].index.tolist()
df = df[df["user_id"].isin(valid_users)]

all_items = set(df["gmap_id"].unique())
print(f"Users: {len(valid_users):,} | Items: {len(all_items):,}")

eval_users = random.sample(valid_users, min(N_EVAL_USERS, len(valid_users)))
print(f"Evaluating on {len(eval_users):,} sampled users")

# Per-user 80/20 split
train_likes = {}   # user_id -> set of gmap_ids (train)
test_items  = {}   # user_id -> one held-out gmap_id

for user_id, group in df[df["user_id"].isin(eval_users)].groupby("user_id"):
    rows = group.sample(frac=1, random_state=RANDOM_SEED)
    split = max(1, int(len(rows) * 0.8))
    train_likes[user_id] = set(rows.iloc[:split]["gmap_id"].tolist())
    held_out = rows.iloc[split:]["gmap_id"].tolist()
    if held_out:
        test_items[user_id] = random.choice(held_out)  # one test item per user

print(f"Test users with held-out item: {len(test_items):,}")

# ── Build CF model ────────────────────────────────────────────────────────────

print("\nBuilding CF model from training split...")
train_df = df[df["user_id"].isin(train_likes)].copy()
# Keep only training interactions (remove held-out)
train_rows = []
for user_id, group in train_df.groupby("user_id"):
    keep = train_likes.get(user_id, set())
    train_rows.append(group[group["gmap_id"].isin(keep)])
train_df = pd.concat(train_rows, ignore_index=True)

user_cat = train_df["user_id"].astype("category")
item_cat = train_df["gmap_id"].astype("category")

train_ui = csr_matrix(
    (train_df["rating"].astype(float), (user_cat.cat.codes, item_cat.cat.codes))
)
train_iu = train_ui.T.tocsr()

uid2idx = dict(zip(user_cat.cat.categories, range(len(user_cat.cat.categories))))
iid2idx = dict(zip(item_cat.cat.categories, range(len(item_cat.cat.categories))))
idx2iid = dict(enumerate(item_cat.cat.categories))

def cf_score_candidates(user_id, candidates):
    if user_id not in uid2idx:
        return {c: 0.0 for c in candidates}
    uidx = uid2idx[user_id]
    user_row = train_ui[uidx]
    liked_indices = user_row.indices
    if len(liked_indices) == 0:
        return {c: 0.0 for c in candidates}
    cand_indices = [iid2idx[c] for c in candidates if c in iid2idx]
    if not cand_indices:
        return {c: 0.0 for c in candidates}
    liked_ratings = user_row.data
    sims = cosine_similarity(train_iu[liked_indices], train_iu[cand_indices])
    for i, iidx in enumerate(liked_indices):
        if iidx in cand_indices:
            j = cand_indices.index(iidx)
            sims[i, j] = 0
    numerator   = sims.T @ liked_ratings
    denominator = sims.sum(axis=0)
    scores = np.divide(numerator, denominator,
                       out=np.zeros_like(numerator, dtype=float),
                       where=denominator != 0)
    return {candidates[j]: float(scores[j]) for j in range(len(cand_indices))}

# ── Load CB model ─────────────────────────────────────────────────────────────

print("Loading CB model...")
with open(MODEL_CB_FILE, "rb") as f:
    cb_model = pickle.load(f)

cb_rests   = cb_model["restaurants"]
tfidf_mat  = cb_model["tfidf_matrix"]
gmap_ids   = cb_rests["gmap_id"].tolist()
gid2cidx   = {g: i for i, g in enumerate(gmap_ids)}

def cb_score_candidates(train_liked, candidates):
    liked_idx = [gid2cidx[g] for g in train_liked if g in gid2cidx]
    cand_idx  = [gid2cidx[c] for c in candidates if c in gid2cidx]
    if not liked_idx or not cand_idx:
        return {c: 0.0 for c in candidates}
    scores = cosine_similarity(tfidf_mat[liked_idx], tfidf_mat[cand_idx]).mean(axis=0)
    return {candidates[j]: float(scores[j]) for j in range(len(cand_idx))}

# ── Generate recommendations ──────────────────────────────────────────────────

print(f"\nEvaluating {len(test_items):,} users with {N_NEGATIVES} negatives each...")

cf_results  = []
cb_results  = []
hyb_results = []

for i, (user_id, positive) in enumerate(test_items.items()):
    if i % 100 == 0:
        print(f"  {i}/{len(test_items)}", end="\r")

    user_all_items = train_likes.get(user_id, set()) | {positive}
    negatives = random.sample(list(all_items - user_all_items), N_NEGATIVES)
    candidates = [positive] + negatives

    # CF
    cf_raw  = cf_score_candidates(user_id, candidates)
    cf_ranked = sorted(candidates, key=lambda c: cf_raw.get(c, 0.0), reverse=True)
    cf_results.append((cf_ranked, positive))

    # CB
    cb_raw  = cb_score_candidates(train_likes.get(user_id, set()), candidates)
    cb_ranked = sorted(candidates, key=lambda c: cb_raw.get(c, 0.0), reverse=True)
    cb_results.append((cb_ranked, positive))

    # Hybrid
    n_likes = len(train_likes.get(user_id, set()))
    alpha   = get_alpha(n_likes)
    cf_n    = normalize(cf_raw)
    cb_n    = normalize(cb_raw)
    hybrid  = {c: alpha * cf_n.get(c, 0.0) + (1 - alpha) * cb_n.get(c, 0.0) for c in candidates}
    hyb_ranked = sorted(candidates, key=lambda c: hybrid.get(c, 0.0), reverse=True)
    hyb_results.append((hyb_ranked, positive))

print(f"  Done.{' '*20}")

# ── Print results ─────────────────────────────────────────────────────────────

print("\n" + "═"*46)
print("  NEGATIVE SAMPLING EVALUATION RESULTS")
print(f"  (1 positive + {N_NEGATIVES} negatives per user)")
print("═"*46)

print_results("Collaborative Filtering (Item-Based CF)", evaluate(cf_results,  K_VALUES))
print_results("Content-Based Filtering (TF-IDF)",       evaluate(cb_results,  K_VALUES))
print_results("Hybrid (Adaptive Alpha)",                 evaluate(hyb_results, K_VALUES))

print(f"\nEvaluated on {len(test_items):,} users | {N_NEGATIVES+1} candidates per user\n")
