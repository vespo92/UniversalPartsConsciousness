# Complete Setup Guide

## Step-by-Step Setup

### 1. Supabase Setup (5 minutes)

1. **Create Account**
   - Go to [supabase.com](https://supabase.com)
   - Sign up or log in

2. **Create New Project**
   - Click "New Project"
   - Choose a name (e.g., "parts-database")
   - Set a strong database password (save this!)
   - Choose a region close to you
   - Click "Create new project"
   - Wait 2-3 minutes for setup to complete

3. **Get API Credentials**
   - Go to Settings (gear icon) > API
   - Copy these two values:
     - Project URL (e.g., `https://xxxxx.supabase.co`)
     - `anon` `public` key (long string starting with `eyJ...`)

4. **Set Up Database Schema**
   - Go to SQL Editor (in left sidebar)
   - Click "New Query"
   - Copy the entire contents of `supabase/schema.sql`
   - Paste into the editor
   - Click "Run" (or press Ctrl/Cmd + Enter)
   - You should see "Success. No rows returned"

5. **Verify Tables Were Created**
   - Go to Table Editor (in left sidebar)
   - You should see tables like `parts`, `thread_specifications`, etc.

### 2. Local Development Setup

1. **Install Node.js** (if not already installed)
   - Download from [nodejs.org](https://nodejs.org)
   - Use version 18 or higher

2. **Clone and Install**
   ```bash
   cd parts-database
   npm install
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env.local
   ```

   Edit `.env.local` and replace the placeholders:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGc...your-long-key-here
   ```

4. **Start Development Server**
   ```bash
   npm run dev
   ```

5. **Open in Browser**
   - Navigate to [http://localhost:3000](http://localhost:3000)
   - You should see the Universal Parts Database interface

### 3. Vercel Deployment (Optional)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial setup"
   git push origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New..." > "Project"
   - Import your GitHub repository
   - Vercel will auto-detect Next.js
   - Add environment variables:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - Click "Deploy"

3. **Done!**
   - Your app will be live at `https://your-project.vercel.app`

## Testing the Setup

### Test 1: Search Parts
1. Go to home page
2. You should see the search interface
3. The search will work but return no results (database is empty)

### Test 2: Add a Part
1. Click "Add Part" button
2. Fill in the form:
   - Manufacturer: "Test"
   - Part Number: "M3x12"
   - Category: "Fastener"
   - Thread Size: "M3x0.5"
   - Length: "12"
3. Click "Add Part"
4. You should see a success message

### Test 3: Search for Your Part
1. Go back to home
2. Search for "M3"
3. Your test part should appear

### Test 4: Check Compatibility
1. Click "Check Compatibility" tab
2. Enter:
   - Screw Thread: "M3x0.5"
   - Screw Length: "12"
   - Hole Thread: "M3x0.5"
   - Material Thickness: "8"
3. Click "Check Compatibility"
4. Should show compatibility analysis

## Troubleshooting

### "Failed to fetch" errors
- Check that `.env.local` has correct Supabase URL and key
- Make sure you ran the schema SQL in Supabase
- Restart the dev server after changing `.env.local`

### Database errors
- Verify schema was run successfully in SQL Editor
- Check Supabase dashboard for any error messages
- Ensure RLS (Row Level Security) policies were created

### Build errors
- Run `npm install` again
- Delete `node_modules` and `.next` folders, then reinstall
- Check Node.js version is 18+

## Next Steps

1. **Add Real Data**
   - Start adding real parts you use
   - Import data from manufacturer catalogs
   - Contribute specs you've measured

2. **Customize**
   - Modify categories to match your needs
   - Add custom fields in the database
   - Adjust the UI to your preferences

3. **Share**
   - Invite others to contribute
   - Share your deployment URL
   - Build the community database together

## Need Help?

- Check the main README.md
- Open an issue on GitHub
- Review Supabase docs: [supabase.com/docs](https://supabase.com/docs)
- Review Next.js docs: [nextjs.org/docs](https://nextjs.org/docs)
