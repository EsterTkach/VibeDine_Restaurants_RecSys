# VibeDine — Claude Instructions

## CRITICAL RULES
- **DO NOT touch the backend** — no changes to `api/`, `src/` (ML code), `requirements.txt`, or any Python files.
- **DO NOT touch the database** — no changes to MongoDB schema, connections, or data.
- **Frontend only** — all work happens inside the `frontend/` directory.

---

## Project Overview

VibeDine is a restaurant recommendation system for California (43,777 restaurants, 15M+ Google reviews).  
It uses a hybrid ML engine (content-based + collaborative filtering) to power personalized recommendations.

**Our responsibility: the frontend web application.**

Design inspiration: **Wolt / Netflix** — horizontal scrollable "trains" of restaurant cards, clean light theme.

---

## Architecture

```
VibeDine_Restaurants_RecSys-aya/
├── api/                    # FastAPI backend (DO NOT TOUCH)
├── src/                    # ML recommendation models (DO NOT TOUCH)
├── frontend/               # React frontend (our work)
│   ├── src/
│   │   ├── types/index.ts          # TypeScript interfaces
│   │   ├── data/mockData.ts        # Mock restaurant data (8 themed rows)
│   │   ├── api/
│   │   │   ├── client.ts           # Axios HTTP client (proxy → localhost:8000)
│   │   │   └── restaurants.ts      # API call functions
│   │   ├── components/
│   │   │   ├── Navbar.tsx          # Top bar: logo, search, profile link
│   │   │   ├── RestaurantCard.tsx  # Card: image, name, rating, category, price
│   │   │   └── RestaurantRow.tsx   # Horizontal scroll row with arrow buttons
│   │   └── pages/
│   │       ├── HomePage.tsx        # Main page with all restaurant rows
│   │       └── ProfilePage.tsx     # User profile, liked places, preferences
│   └── package.json
├── CLAUDE.md               # This file
└── README.md
```

---

## How to Run

### Frontend (our work)
```bash
cd frontend
npm install       # first time only
npm run dev       # starts at http://localhost:5173
```

### Backend (not our responsibility — for reference only)
```bash
# Requires Python environment + data files in data/ folder
uvicorn api.main:app --reload
# Runs at http://localhost:8000
```

---

## Backend API Reference (read-only — do not modify)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/recommend/cf/{user_id}` | CF recommendations for a user |
| `GET` | `/recommend/cb/{restaurant_name}` | Similar restaurants (content-based) |
| `POST` | `/users/signup` | Create new user `{username}` |
| `GET` | `/users/test-db` | Test DB connection |

The Vite dev server proxies `/api/*` → `http://localhost:8000/*`.

To switch from mock data to real API: change `USE_MOCK = true` to `false` in `frontend/src/api/restaurants.ts`.

---

## Tech Stack (Frontend)

| Tool | Version | Purpose |
|------|---------|---------|
| React | 18 | UI framework |
| Vite | 8 | Dev server + bundler |
| TypeScript | 5 | Type safety |
| Tailwind CSS | 4 (via @tailwindcss/vite) | Styling |
| React Router | 6 | Page routing |
| Axios | latest | HTTP requests |

---

## Current Status — Feature Checklist

### Pages
- [x] **Homepage** — horizontal scrollable rows of restaurant cards (Wolt/Netflix style)
- [x] **Profile page** — user info, liked places, preferences, account settings
- [x] **Restaurant detail page** — `/restaurant/:id`, shows image, name, category, rating, price, open status, service/dining options

### Components
- [x] **Navbar** — logo, search bar, profile link
- [x] **RestaurantCard** — image, name, category, rating (stars + number), price level, open/closed badge
- [x] **RestaurantRow** — titled section with left/right arrow scroll buttons

### Features from PDF
- [x] Themed recommendation rows (Italian, laptop-friendly, groups, morning coffee, date night, etc.)
- [x] Search/filter restaurants by name or category
- [x] User profile with liked places
- [x] Preferences panel (dietary filters: vegan, vegetarian, gluten-free; dine-in/takeout; laptop-friendly)
- [x] Invite friends button
- [x] Price level indicator (`$` / `$$` / `$$$` / `$$$$`)
- [x] Open/Closed status badge on cards
- [x] Restaurant detail page — clicking a card navigates to `/restaurant/:id`
- [ ] Real API integration (currently using mock data — `USE_MOCK = true`)
- [ ] Search by time (open now / future time) — requires backend support
- [ ] Filter by location radius — requires geolocation + backend support
- [ ] Group recommendation flow (multiple user preferences) — requires backend support
- [ ] Weather-aware recommendations — requires weather API
- [ ] Budget filter slider
- [ ] Allergy/dietary filter connected to backend
- [ ] Payment method filter
- [ ] Dine-in / takeout filter connected to backend
- [ ] Accessibility filter
- [ ] Context-aware ("where should I go?") — requires LLM integration
- [ ] Laptop suitability score — requires backend field

### Infrastructure
- [x] Vite dev server with proxy to backend (`/api` → `localhost:8000`)
- [x] TypeScript build passes with zero errors
- [x] Mock data for all 8 restaurant row categories
- [ ] Authentication / persistent user sessions (currently hardcoded mock user)

---

## Key Design Decisions

1. **Mock data first** — frontend works without backend running. Flip `USE_MOCK` when backend is ready.
2. **Orange accent color** (`#f97316`) — warm, food-appropriate brand color.
3. **No custom CSS files** — all styling via Tailwind utility classes.
4. **Horizontal scroll** — `overflow-x-auto` with hidden scrollbar + arrow button navigation.
5. **Item-based approach** — rows are themed by restaurant characteristics (matches PDF decision to go Item-based).

---

## Adding a New Feature

1. **New row category**: Add entry to `MOCK_ROWS` in `frontend/src/data/mockData.ts`
2. **New page**: Create `frontend/src/pages/NewPage.tsx`, add `<Route>` in `App.tsx`
3. **New component**: Create `frontend/src/components/NewComponent.tsx`
4. **Connect to real API**: Update functions in `frontend/src/api/restaurants.ts`

---

## Last Updated
2026-05-26 — Color theme updated (#264653 / #069494 / #FFC0CB / #FCE883 / #F1FAEE), fonts changed to Parisienne + Nunito, full-width layout, SVG search icon fixed, restaurant detail page added.
