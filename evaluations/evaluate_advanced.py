"""
VibeDine — Advanced Evaluation Script
======================================
Three complementary evaluations that demonstrate the system's quality beyond
simple hit-rate metrics:

  1. Cold-Start vs Warm User Analysis
     Hit Rate@20 broken down by the user's number of training interactions.
     Shows that the hybrid improves as users accumulate more likes — directly
     validating the adaptive-alpha design decision.

  2. Personalization Score
     Measures how different recommendations are across users.
     A system that gives everyone the same list is not personalizing.

  3. Beyond Popularity — Does the System Surprise?
     Compares recommendations to a pure popularity baseline.
     Shows the system recommends items users wouldn't find by just browsing
     the most popular restaurants.

Run from the project root:
    py evaluate_advanced.py
"""

import pickle
import random
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations

# ── Config ────────────────────────────────────────────────────────────────────

INTERACTIONS_FILE = "data/CF_interaction_matrix_1.parquet"
MODEL_CB_FILE     = "models/content_based_model.pkl"
MIN_RATING        = 4
MIN_INTERACTIONS  = 5
N_EVAL_USERS      = 1000
TOP_K             = 20
RANDOM_SEED       = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize(scores):
    if not scores:
        return {}
    vals = np.array(list(scores.values()), dtype=float)
    mn, mx = vals.min(), vals.max()
    if mx == mn:
        return {k: 0.5 for k in scores}
    return {k: float((v - mn) / (mx - mn)) for k, v in scores.items()}

def get_alpha(n):
    if n <= 5:   return 0.0
    if n <= 20:  return 0.4
    if n <= 100: return 0.7
    return 0.85

def hit_rate_at_k(ranked, positive, k):
    return 1.0 if positive in ranked[:k] else 0.0

def section(title):
    print(f"\n{'═'*56}")
    print(f"  {title}")
    print(f"{'═'*56}")

# ── Load data ─────────────────────────────────────────────────────────────────

print("Loading data...")
df = pd.read_parquet(INTERACTIONS_FILE)
df = df[df["rating"] >= MIN_RATING][["user_id", "gmap_id", "rating"]].copy()

counts      = df.groupby("user_id").size()
valid_users = counts[counts >= MIN_INTERACTIONS].index.tolist()
df          = df[df["user_id"].isin(valid_users)]
all_items   = list(df["gmap_id"].unique())

eval_users = random.sample(valid_users, min(N_EVAL_USERS, len(valid_users)))
eval_set   = set(eval_users)
print(f"Loaded {len(valid_users):,} users | {len(all_items):,} items | evaluating {len(eval_users):,} users")

# Per-user 80/20 split
train_likes = {}
test_item   = {}

for user_id, group in df[df["user_id"].isin(eval_set)].groupby("user_id"):
    rows  = group.sample(frac=1, random_state=RANDOM_SEED)
    split = max(1, int(len(rows) * 0.8))
    train_likes[user_id] = set(rows.iloc[:split]["gmap_id"].tolist())
    held  = rows.iloc[split:]["gmap_id"].tolist()
    if held:
        test_item[user_id] = random.choice(held)

# ── Build CF model ────────────────────────────────────────────────────────────

print("Building CF model...")
train_rows = []
for uid, group in df[df["user_id"].isin(eval_set)].groupby("user_id"):
    keep = train_likes.get(uid, set())
    train_rows.append(group[group["gmap_id"].isin(keep)])
train_df = pd.concat(train_rows, ignore_index=True)

user_cat = train_df["user_id"].astype("category")
item_cat = train_df["gmap_id"].astype("category")
train_ui = csr_matrix(
    (train_df["rating"].astype(float), (user_cat.cat.codes, item_cat.cat.codes))
)
train_iu  = train_ui.T.tocsr()
uid2idx   = dict(zip(user_cat.cat.categories, range(len(user_cat.cat.categories))))
iid2idx   = dict(zip(item_cat.cat.categories, range(len(item_cat.cat.categories))))
idx2iid   = dict(enumerate(item_cat.cat.categories))

def cf_scores(user_id):
    if user_id not in uid2idx:
        return {}
    uidx         = uid2idx[user_id]
    user_row     = train_ui[uidx]
    liked_idx    = user_row.indices
    if len(liked_idx) == 0:
        return {}
    liked_ratings = user_row.data
    sims          = cosine_similarity(train_iu[liked_idx], train_iu)
    for i, iidx in enumerate(liked_idx):
        sims[i, iidx] = 0
    numerator   = sims.T @ liked_ratings
    denominator = sims.sum(axis=0)
    scores = np.divide(numerator, denominator,
                       out=np.zeros_like(numerator, dtype=float),
                       where=denominator != 0)
    liked_set = set(liked_idx)
    return {idx2iid[i]: float(scores[i]) for i in range(len(scores)) if i not in liked_set}

# ── Load CB model ─────────────────────────────────────────────────────────────

print("Loading CB model...")
with open(MODEL_CB_FILE, "rb") as f:
    cb_model = pickle.load(f)

cb_rests  = cb_model["restaurants"]
tfidf_mat = cb_model["tfidf_matrix"]
gmap_ids  = cb_rests["gmap_id"].tolist()
gid2cidx  = {g: i for i, g in enumerate(gmap_ids)}

def cb_scores(train_liked):
    liked_idx = [gid2cidx[g] for g in train_liked if g in gid2cidx]
    if not liked_idx:
        return {}
    raw = cosine_similarity(tfidf_mat[liked_idx], tfidf_mat).mean(axis=0)
    liked_set = set(train_liked)
    return {gmap_ids[i]: float(raw[i]) for i in range(len(raw))
            if gmap_ids[i] not in liked_set}

def hybrid_topk(user_id, k=TOP_K):
    train    = train_likes.get(user_id, set())
    n_likes  = len(train)
    alpha    = get_alpha(n_likes)
    cf_n     = normalize(cf_scores(user_id))
    cb_n     = normalize(cb_scores(train))
    all_ids  = set(cf_n) | set(cb_n)
    hybrid   = {g: alpha * cf_n.get(g, 0.0) + (1 - alpha) * cb_n.get(g, 0.0)
                for g in all_ids}
    return sorted(hybrid, key=hybrid.get, reverse=True)[:k]

def cb_topk(user_id, k=TOP_K):
    train = train_likes.get(user_id, set())
    s = normalize(cb_scores(train))
    return sorted(s, key=s.get, reverse=True)[:k]

# ── Popularity baseline ───────────────────────────────────────────────────────

pop_counts   = df["gmap_id"].value_counts()
popular_list = pop_counts.index.tolist()

# ═══════════════════════════════════════════════════════════════
# TEST 1 — Cold Start vs Warm User Analysis
# ═══════════════════════════════════════════════════════════════

section("TEST 1 — Cold Start vs Warm User: Hit Rate@20 by Interaction Count")

buckets = {
    "1–5 likes (cold start)":  (1,   5),
    "6–20 likes":               (6,  20),
    "21–100 likes":             (21, 100),
    "100+ likes (warm)":        (101, 9999),
}

bucket_results = {name: {"cb": [], "hybrid": []} for name in buckets}

users_evaluated = 0
for i, (user_id, pos) in enumerate(test_item.items()):
    if i % 100 == 0:
        print(f"  {i}/{len(test_item)}", end="\r")

    n = len(train_likes.get(user_id, set()))

    for name, (lo, hi) in buckets.items():
        if lo <= n <= hi:
            cb_rec  = cb_topk(user_id)
            hyb_rec = hybrid_topk(user_id)
            bucket_results[name]["cb"].append(hit_rate_at_k(cb_rec, pos, TOP_K))
            bucket_results[name]["hybrid"].append(hit_rate_at_k(hyb_rec, pos, TOP_K))
            users_evaluated += 1

print(f"  Done.{' '*20}")
print(f"\n  {'User Group':<28}  {'N Users':>8}  {'CB HR@20':>10}  {'Hybrid HR@20':>13}")
print(f"  {'─'*28}  {'─'*8}  {'─'*10}  {'─'*13}")
for name, res in bucket_results.items():
    n = len(res["cb"])
    if n == 0:
        continue
    cb_hr  = np.mean(res["cb"])
    hyb_hr = np.mean(res["hybrid"])
    winner = "← Hybrid wins" if hyb_hr > cb_hr else ("← CB wins" if cb_hr > hyb_hr else "← Tie")
    print(f"  {name:<28}  {n:>8}  {cb_hr:>10.4f}  {hyb_hr:>13.4f}  {winner}")

print("\n  Insight: Hybrid should improve over CB as users accumulate more interactions,")
print("  validating the adaptive-alpha design decision.")

# ═══════════════════════════════════════════════════════════════
# TEST 2 — Personalization Score
# ═══════════════════════════════════════════════════════════════

section("TEST 2 — Personalization Score")

print("  Sampling 200 users for pairwise comparison...")
sample_users = random.sample(list(test_item.keys()), min(200, len(test_item)))

cb_lists  = {}
hyb_lists = {}
pop_list  = set(popular_list[:TOP_K])

for i, uid in enumerate(sample_users):
    if i % 20 == 0:
        print(f"  {i}/{len(sample_users)}", end="\r")
    cb_lists[uid]  = set(cb_topk(uid))
    hyb_lists[uid] = set(hybrid_topk(uid))

print(f"  Done.{' '*20}")

def personalization(lists_dict):
    """Average pairwise dissimilarity between top-K lists."""
    users = list(lists_dict.keys())
    diffs = []
    for u1, u2 in random.sample(list(combinations(users, 2)), min(2000, len(users)*(len(users)-1)//2)):
        s1, s2 = lists_dict[u1], lists_dict[u2]
        overlap = len(s1 & s2) / TOP_K
        diffs.append(1 - overlap)
    return np.mean(diffs)

# Popularity baseline "personalization" (everyone gets same list)
pop_dict = {uid: pop_list for uid in sample_users}

cb_score  = personalization(cb_lists)
hyb_score = personalization(hyb_lists)
pop_score = personalization(pop_dict)

print(f"\n  {'Model':<30}  {'Personalization Score':>22}")
print(f"  {'─'*30}  {'─'*22}")
print(f"  {'Popularity Baseline':<30}  {pop_score:>22.4f}  (0 = everyone gets same list)")
print(f"  {'Content-Based (TF-IDF)':<30}  {cb_score:>22.4f}")
print(f"  {'Hybrid (Adaptive α)':<30}  {hyb_score:>22.4f}")
print(f"\n  Score = avg pairwise dissimilarity in top-{TOP_K} lists (higher = more personalized).")
print(f"  A score of 1.0 means no two users share any recommendation.")

# ═══════════════════════════════════════════════════════════════
# TEST 3 — Beyond Popularity
# ═══════════════════════════════════════════════════════════════

section("TEST 3 — Beyond Popularity: Does the System Surprise?")

print("  Computing overlap with top-K popularity baseline...")

top_popular = set(popular_list[:TOP_K])

cb_overlaps  = []
hyb_overlaps = []

for uid in sample_users:
    cb_set  = cb_lists[uid]
    hyb_set = hyb_lists[uid]
    cb_overlaps.append(len(cb_set  & top_popular) / TOP_K)
    hyb_overlaps.append(len(hyb_set & top_popular) / TOP_K)

cb_overlap  = np.mean(cb_overlaps)
hyb_overlap = np.mean(hyb_overlaps)

print(f"\n  What fraction of each model's top-{TOP_K} overlaps with the {TOP_K} most popular restaurants?\n")
print(f"  {'Model':<30}  {'Overlap with Popularity':>24}")
print(f"  {'─'*30}  {'─'*24}")
print(f"  {'Popularity Baseline':<30}  {'100.00%':>24}  (by definition)")
print(f"  {'Content-Based (TF-IDF)':<30}  {cb_overlap*100:>23.1f}%")
print(f"  {'Hybrid (Adaptive α)':<30}  {hyb_overlap*100:>23.1f}%")

print(f"\n  Lower overlap = the system personalizes beyond just recommending")
print(f"  what everyone else likes. High overlap would mean the system")
print(f"  is equivalent to a simple popularity ranker.")

print(f"\n{'═'*56}")
print(f"  All tests complete.")
print(f"{'═'*56}\n")
