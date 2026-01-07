import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  try {
    const supabaseClient = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    const { data: allReviews, error } = await supabaseClient
      .from("reviews")
      .select("rating, created_at");

    if (error) throw error;

    const totalReviews = allReviews?.length || 0;
    
    const avgRating = totalReviews > 0
      ? allReviews.reduce((sum, r) => sum + r.rating, 0) / totalReviews
      : 0;

    const ratingDistribution: Record<number, number> = {};
    for (let i = 1; i <= 5; i++) {
      ratingDistribution[i] = allReviews?.filter(r => r.rating === i).length || 0;
    }

    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const recentCount = allReviews?.filter(
      r => new Date(r.created_at) >= yesterday
    ).length || 0;

    return new Response(
      JSON.stringify({
        total_reviews: totalReviews,
        average_rating: Math.round(avgRating * 100) / 100,
        rating_distribution: ratingDistribution,
        recent_reviews_count: recentCount,
      }),
      {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      }
    );
  }
});