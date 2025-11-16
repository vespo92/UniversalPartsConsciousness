# Universal Parts Database

A comprehensive, searchable database for mechanical parts with Bill of Materials (BOM) support and compatibility checking. Never lose a screw again!

## Features

- **Part Search**: Find parts by thread size, manufacturer, part number, or specifications
- **Compatibility Checker**: Verify if parts will work together with detailed analysis
- **User Contributions**: Add new parts to the community database
- **BOM Support**: Link parts together in Bill of Materials for complete products
- **Open Source**: Built on open standards and open to community contributions

## Tech Stack

- **Frontend**: Next.js 15 with TypeScript and Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **Hosting**: Vercel
- **Authentication**: Supabase Auth (for user contributions)

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd parts-database
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Copy your project URL and anon key from Settings > API
3. Go to the SQL Editor in your Supabase dashboard
4. Run the schema from `supabase/schema.sql`

### 4. Configure Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your Supabase credentials:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 5. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Deploy to Vercel

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/parts-database)

### Manual Deploy

1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com) and import your repository
3. Add environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
4. Deploy!

## Database Schema

The database includes tables for:

- **Parts**: Core part specifications with full dimensional data
- **Thread Specifications**: Detailed thread dimensions and tolerances
- **Fastener Heads**: Head and drive specifications
- **Material Compatibility**: Material interaction data
- **Thread Compatibility**: Thread fit analysis
- **Installation Requirements**: Torque specs and tooling
- **Products**: Product definitions
- **BOM Items**: Bill of materials linking parts to products
- **User Contributions**: Community-submitted data

See `supabase/schema.sql` for the complete schema.

## Usage Examples

### Search for Parts

1. Navigate to the home page
2. Enter search criteria (thread size, part number, etc.)
3. Browse results and click to see detailed specifications

### Check Compatibility

1. Click the "Check Compatibility" tab
2. Enter screw thread size and length
3. Enter hole thread size and material thickness
4. Click "Check Compatibility" to see analysis

### Add a New Part

1. Click "Add Part" in the header
2. Fill in the form with part specifications
3. Submit to add to the database

## Contributing

We welcome contributions! Here's how you can help:

1. **Add Parts**: Use the contribute form to add parts you know about
2. **Improve Data**: Submit corrections or additional specifications
3. **Code Contributions**: Submit PRs for new features or bug fixes
4. **Documentation**: Help improve docs and examples

## Data Sources

This project aims to aggregate data from:

- Manufacturing standards (ISO, DIN, ANSI, JIS)
- Open-source CAD libraries
- Manufacturer catalogs
- Community contributions
- Reverse-engineered specifications

## Roadmap

- [ ] Add authentication for user accounts
- [ ] Implement parts verification workflow
- [ ] Add image uploads for parts
- [ ] Create mobile app
- [ ] Integrate with CAD software
- [ ] Add API for programmatic access
- [ ] Implement advanced search with filters
- [ ] Add product BOM management interface
- [ ] Create compatibility matrix visualizations
- [ ] Add strength calculation tools

## License

MIT License - see LICENSE file for details

## Support

For questions or issues, please [open an issue](https://github.com/yourusername/parts-database/issues) on GitHub.

## Acknowledgments

Built with the goal of making mechanical engineering and repair work easier for everyone. Special thanks to all contributors who help build the world's most comprehensive parts database.
