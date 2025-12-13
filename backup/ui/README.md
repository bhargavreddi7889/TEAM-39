# CampusOps AI - Frontend

A modern, role-based React frontend for the CampusOps AI system with separate interfaces for Students and Administrators.

## Features

### 🎓 Student Portal
- **Interactive Chat Interface**: Ask questions about campus policies with a clean, intuitive chat UI
- **Multiple Queries**: Ask as many questions as needed in a continuous conversation
- **Source Citations**: View the exact policy sources used to generate each answer
- **Graceful Error Handling**: Clear messaging when information is not found
- **Real-time Responses**: Get instant AI-powered answers to policy questions

### 👨‍💼 Admin Portal
- **Document Upload**: Upload policy documents in TXT or PDF format
- **Knowledge Base Management**: View and manage all uploaded documents
- **Real-time Statistics**: Track total chunks and document count
- **File Processing**: Automatic chunking and indexing of uploaded files
- **Dashboard Overview**: Monitor system status and usage

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icon library
- **CSS3** - Modern styling with CSS variables

## Prerequisites

- Node.js 16+ and npm
- Backend API running on http://localhost:8000

## Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable components (future)
│   ├── context/
│   │   └── AuthContext.jsx  # Authentication context
│   ├── pages/
│   │   ├── Login.jsx        # Login page with role selection
│   │   ├── StudentDashboard.jsx  # Student query interface
│   │   └── AdminDashboard.jsx    # Admin document management
│   ├── utils/
│   │   └── api.js           # API client and endpoints
│   ├── App.jsx              # Main app with routing
│   ├── main.jsx             # React entry point
│   └── index.css            # Global styles
├── index.html
├── vite.config.js
└── package.json
```

## Usage

### Demo Credentials

The system includes demo authentication:

**Student Login:**
- Username: `student`
- Password: `student123`

**Admin Login:**
- Username: `admin`
- Password: `admin123`

### Student Workflow

1. Login with student credentials
2. Type your question about campus policies in the chat input
3. View the AI-generated answer with source citations
4. Continue asking questions - conversation history is maintained
5. Click on suggested questions for quick queries

### Admin Workflow

1. Login with admin credentials
2. View knowledge base statistics on the dashboard
3. Click "Choose File" to select a TXT or PDF document
4. Click "Upload" to process and add the document to the knowledge base
5. View the list of uploaded documents
6. Monitor the total chunks in the system

## API Integration

The frontend communicates with the backend via these endpoints:

- `POST /api/query/` - Submit student questions
- `GET /api/health` - Get system status and chunk count
- `POST /api/admin/ingest/file` - Upload document files
- `GET /api/admin/stats` - Get knowledge base statistics
- `GET /api/admin/documents` - List all documents
- `DELETE /api/admin/documents/:id` - Delete a document

## Features in Detail

### Authentication System
- Role-based access control (Student/Admin)
- Persistent sessions using localStorage
- Protected routes with automatic redirects
- Secure logout functionality

### Student Interface
- Chat-like UI with message history
- User and bot message differentiation
- Typing indicators during processing
- Expandable source citations
- Suggested questions for first-time users
- Responsive design for mobile devices

### Admin Interface
- File upload with drag-and-drop ready design
- Support for both TXT and PDF files
- Real-time upload progress
- Success/error notifications
- Document listing with metadata
- Statistics dashboard with refresh capability

## Styling

The app uses CSS variables for consistent theming:

```css
--primary: #2563eb      /* Primary blue */
--secondary: #64748b    /* Secondary gray */
--success: #10b981      /* Success green */
--danger: #ef4444       /* Error red */
--light: #f8fafc        /* Light background */
--dark: #0f172a         /* Dark text */
```

## Build for Production

To create a production build:

```bash
npm run build
```

The optimized files will be in the `dist/` directory.

To preview the production build:

```bash
npm run preview
```

## Environment Configuration

The frontend uses Vite's proxy configuration to forward API requests to the backend:

```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true
  }
}
```

For production, update the API base URL in `src/utils/api.js`.

## Future Enhancements

- [ ] Real authentication with JWT tokens
- [ ] Document editing capabilities
- [ ] Advanced search and filtering
- [ ] User management for admins
- [ ] Analytics and usage statistics
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Voice input for queries
- [ ] Export conversation history
- [ ] Real-time collaboration

## Troubleshooting

**Issue: Frontend can't connect to backend**
- Ensure backend is running on port 8000
- Check CORS configuration in backend
- Verify proxy settings in vite.config.js

**Issue: Login not working**
- Clear localStorage and try again
- Check browser console for errors
- Verify credentials match demo accounts

**Issue: File upload fails**
- Check file format (only .txt and .pdf)
- Ensure file size is reasonable
- Check backend logs for errors

## Contributing

When contributing to the frontend:

1. Follow the existing code structure
2. Use functional components with hooks
3. Maintain consistent styling patterns
4. Add comments for complex logic
5. Test on multiple browsers
6. Ensure mobile responsiveness

## License

Part of the CampusOps AI project for JNTU Vijayanagaram Hackathon.

