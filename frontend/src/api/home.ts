import { getHomeCarousels } from "./restaurants";

export async function preloadHomeData(user_id: string) {
  try {
    const data = await getHomeCarousels(user_id);

    sessionStorage.setItem(
      "home_carousels",
      JSON.stringify(data)
    );
  } catch (error) {
    console.error("Failed to preload home data:", error);
  }
}