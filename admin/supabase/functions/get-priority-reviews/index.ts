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

    const url = new URL(req.url);
    const limit = Math.min(parseInt(url.searchParams.get("limit") || "20"), 100);

    const { data: urgentReviews, error } = await supabaseClient
      .from("reviews")
      .select("*")
      .in("rating", [1, 2])
      .order("created_at", { ascending: false })
      .limit(limit);

    if (error) throw error;

    const { count: totalUrgent } = await supabaseClient
      .from("reviews")
      .select("*", { count: "exact", head: true })
      .in("rating", [1, 2]);

    return new Response(
      JSON.stringify({
        urgent_reviews: urgentReviews || [],
        total_urgent: totalUrgent || 0,
        message: `Found ${totalUrgent || 0} reviews requiring immediate attention`,
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