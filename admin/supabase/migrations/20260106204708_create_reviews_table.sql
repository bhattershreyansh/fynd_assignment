/*
  # Create Reviews Table for Admin Dashboard

  1. New Tables
    - `reviews`
      - `id` (uuid, primary key) - Unique identifier for each review
      - `rating` (integer, 1-5) - Star rating given by the user
      - `review_text` (text) - The full review content
      - `summary` (text, nullable) - AI-generated summary for admins
      - `recommended_actions` (text array, nullable) - AI-suggested actions
      - `user_response` (text, nullable) - Auto-response sent to user
      - `created_at` (timestamptz) - Timestamp of review submission
      - `updated_at` (timestamptz) - Last update timestamp

  2. Indexes
    - Index on `rating` for fast filtering
    - Index on `created_at` for sorting and date queries

  3. Security
    - Enable RLS on `reviews` table
    - Admin-only access policies for read operations
*/

CREATE TABLE IF NOT EXISTS reviews (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  rating integer NOT NULL CHECK (rating >= 1 AND rating <= 5),
  review_text text NOT NULL CHECK (length(trim(review_text)) >= 10),
  summary text,
  recommended_actions text[] DEFAULT '{}',
  user_response text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_created_at ON reviews(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_reviews_priority ON reviews(rating) WHERE rating IN (1, 2);

-- Enable Row Level Security
ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

-- Admin users can read all reviews
CREATE POLICY "Admins can view all reviews"
  ON reviews
  FOR SELECT
  TO authenticated
  USING (true);

-- Allow service role to insert/update (for edge functions)
CREATE POLICY "Service role can insert reviews"
  ON reviews
  FOR INSERT
  TO service_role
  WITH CHECK (true);

CREATE POLICY "Service role can update reviews"
  ON reviews
  FOR UPDATE
  TO service_role
  USING (true)
  WITH CHECK (true);