# Fraud Detection System - Next.js UI

A modern, responsive web application for fraud detection built with Next.js, TypeScript, and Tailwind CSS.

## 🚀 Features

- **Authentication System**: Secure login with NextAuth.js
- **Modern UI**: Beautiful, responsive design with Tailwind CSS
- **Dashboard**: Real-time statistics and analytics
- **Fraud Detection**: Interactive form for transaction analysis
- **Settings**: Configurable system parameters
- **TypeScript**: Full type safety throughout the application

## 🛠️ Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Authentication**: NextAuth.js
- **Icons**: Lucide React
- **Charts**: Recharts (for future analytics)
- **Backend Integration**: Flask API (your existing ML model)

## 📁 Project Structure

```
fraud-detection-ui/
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth/[...nextauth]/route.ts    # Authentication API
│   │   │   └── predict/route.ts               # Fraud prediction API
│   │   ├── dashboard/
│   │   │   ├── layout.tsx                     # Dashboard layout
│   │   │   ├── page.tsx                       # Dashboard home
│   │   │   ├── detect/page.tsx                # Fraud detection form
│   │   │   └── settings/page.tsx              # Settings page
│   │   ├── login/page.tsx                     # Login page
│   │   ├── layout.tsx                         # Root layout
│   │   ├── page.tsx                           # Home (redirects to login)
│   │   ├── providers.tsx                      # Auth providers
│   │   └── globals.css                        # Global styles
│   └── ...
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Your Flask backend running on port 5000

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Set up environment variables:**
   Create a `.env.local` file in the root directory:
   ```env
   NEXTAUTH_SECRET=your-secret-key-here
   NEXTAUTH_URL=http://localhost:3000
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🔐 Authentication

### Demo Credentials
- **Email**: admin@frauddetection.com
- **Password**: password

### Adding Real Authentication
To integrate with a real database:

1. Install Prisma:
   ```bash
   npm install prisma @prisma/client
   ```

2. Set up your database schema in `prisma/schema.prisma`

3. Update the NextAuth configuration in `src/app/api/auth/[...nextauth]/route.ts`

## 🔗 Backend Integration

The application connects to your Flask backend for fraud predictions:

1. **Start your Flask backend:**
   ```bash
   cd ../app
   python serve_model.py
   ```

2. **The Next.js app will call:**
   - `POST http://localhost:5000/predict` for fraud predictions

3. **API Format:**
   ```json
   {
     "features": [
       "user_id",
       "signup_time", 
       "purchase_time",
       "purchase_value",
       "device_id",
       "source",
       "browser", 
       "sex",
       "age",
       "ip_address"
     ]
   }
   ```

## 📊 Features Overview

### Dashboard
- Real-time statistics cards
- Recent activity feed
- Quick action buttons
- Responsive design

### Fraud Detection
- Comprehensive transaction form
- Real-time prediction results
- Risk factor analysis
- Confidence scoring

### Settings
- Model threshold configuration
- Notification preferences
- API key management
- Database status monitoring

## 🎨 UI Components

The application uses a consistent design system:

- **Colors**: Blue primary, with semantic colors for success/error states
- **Typography**: Clean, readable fonts with proper hierarchy
- **Spacing**: Consistent spacing using Tailwind's scale
- **Icons**: Lucide React icons throughout
- **Responsive**: Mobile-first design approach

## 🔧 Customization

### Styling
- Modify `src/app/globals.css` for global styles
- Update Tailwind config in `tailwind.config.ts`
- Component-specific styles in each component

### Authentication
- Update `src/app/api/auth/[...nextauth]/route.ts` for different providers
- Modify login page in `src/app/login/page.tsx`

### API Integration
- Update `src/app/api/predict/route.ts` for different backend endpoints
- Modify form fields in `src/app/dashboard/detect/page.tsx`

## 🚀 Deployment

### Vercel (Recommended)
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy!

### Other Platforms
- **Netlify**: Use `npm run build` and deploy the `out` directory
- **Docker**: Create a Dockerfile and deploy to any container platform

## 🔒 Security Considerations

- Environment variables for sensitive data
- HTTPS in production
- Input validation on all forms
- Rate limiting for API endpoints
- Regular dependency updates

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues or questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include steps to reproduce the problem

---

**Built with ❤️ using Next.js, TypeScript, and Tailwind CSS**
