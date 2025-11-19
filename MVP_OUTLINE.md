# Diane MVP Outline

## Overview
Diane is a mental load management application that helps users capture brain dumps and automatically categorizes them into tasks, shopping items, and calendar events using AI.

## MVP Goals
- Simple email-based authentication (future: Google OAuth)
- Landing page with 4 tabs: Home, Tasks, Shopping, Calendar
- Brain dump processing with AI categorization
- Basic CRUD operations for all item types

---

## Current State

### ✅ Backend - Already Implemented
- FastAPI backend with PostgreSQL database
- Email-based login endpoint (`POST /auth/login`)
- Brain dump processing endpoint (`POST /brain-dumps/`)
- Claude AI integration for categorization and task decomposition
- Database models: User, Task, SubTask, ShoppingItem, CalendarEvent
- Create operations for all item types

### ✅ Frontend - Already Implemented
- React + TypeScript + Vite setup
- Axios API client with error handling
- Zustand state management for users
- TypeScript interfaces and domain models
- API functions for login and brain dump processing

### ❌ What's Missing
- Frontend UI components and pages
- Backend GET/UPDATE/DELETE endpoints
- Routing configuration
- Additional state management stores
- Completion/update functionality

---

## MVP Task Breakdown

### Phase 1: Backend API Completion

#### 1.1 Task Endpoints
- [ ] **GET /tasks/:user_id** - Retrieve all tasks for a user
  - Query params: `completed` (optional filter), `sort_by` (due_date, created_at)
  - Response: List of tasks with subtasks
- [ ] **GET /tasks/:id** - Retrieve single task with subtasks
- [ ] **PUT /tasks/:id** - Update task details
  - Allow updates: description, due_date, estimated_time_minutes, completed
- [ ] **DELETE /tasks/:id** - Delete task (cascade to subtasks)
- [ ] **PUT /tasks/:task_id/subtasks/:subtask_id** - Update subtask
  - Allow updates: description, completed, due_date, estimated_time_minutes
- [ ] **DELETE /tasks/:task_id/subtasks/:subtask_id** - Delete subtask

#### 1.2 Shopping Item Endpoints
- [ ] **GET /shopping-items/:user_id** - Retrieve all shopping items
  - Query params: `completed` (optional filter)
- [ ] **PUT /shopping-items/:id** - Update shopping item
  - Allow updates: description, completed
- [ ] **DELETE /shopping-items/:id** - Delete shopping item

#### 1.3 Calendar Event Endpoints
- [ ] **GET /calendar-events/:user_id** - Retrieve all calendar events
  - Query params: `start_date`, `end_date` (optional date range filter)
  - Sort by: event_date, event_time
- [ ] **PUT /calendar-events/:id** - Update calendar event
  - Allow updates: description, event_date, event_time
- [ ] **DELETE /calendar-events/:id** - Delete calendar event

#### 1.4 Authentication Enhancement
- [ ] Add basic session/token validation (simple JWT or API key)
- [ ] Protect endpoints to ensure users can only access their own data
- [ ] Add middleware to validate user_id from token

---

### Phase 2: Frontend - Core Pages & Components

#### 2.1 Authentication UI
- [ ] **Login Page** (`/login`)
  - Email input field
  - Login button
  - Call `POST /auth/login` on submit
  - Store user in Zustand store
  - Redirect to home on success
- [ ] **Protected Route Wrapper**
  - Check if user exists in store
  - Redirect to login if not authenticated
- [ ] **Logout Functionality**
  - Clear user from store
  - Redirect to login

#### 2.2 Layout & Navigation
- [ ] **Main Layout Component**
  - Header with app name and logout button
  - Tab navigation: Home, Tasks, Shopping, Calendar
  - Render active tab content
- [ ] **React Router Setup**
  - `/login` - Login page
  - `/` - Home page (protected)
  - `/tasks` - Tasks page (protected)
  - `/shopping` - Shopping page (protected)
  - `/calendar` - Calendar page (protected)

#### 2.3 Home Page (Brain Dump)
- [ ] **Brain Dump Form**
  - Large textarea for free-form text input
  - Submit button
  - Loading state while processing
- [ ] **Brain Dump Results Display**
  - Show categorized results after submission
  - Display tasks (with subtasks), shopping items, calendar events
  - Success message
  - Option to clear and create new brain dump
- [ ] **Zustand Store for Brain Dumps**
  - Store latest brain dump result
  - Clear function

#### 2.4 Tasks Page
- [ ] **Zustand Store for Tasks**
  - State: tasks array, loading, error
  - Actions: fetchTasks, updateTask, deleteTask, toggleTaskCompletion
- [ ] **Task List Component**
  - Fetch tasks on mount
  - Display all tasks grouped by completed/incomplete
  - Show due dates, estimated time
  - Expand/collapse subtasks
- [ ] **Task Item Component**
  - Checkbox to mark complete/incomplete
  - Display description, due date
  - Edit button (inline or modal)
  - Delete button with confirmation
  - Subtask list with individual completion toggles
- [ ] **Task Filter/Sort**
  - Filter: All, Active, Completed
  - Sort: Due date, Created date

#### 2.5 Shopping Page
- [ ] **Zustand Store for Shopping Items**
  - State: shopping_items array, loading, error
  - Actions: fetchShoppingItems, updateItem, deleteItem, toggleCompletion
- [ ] **Shopping List Component**
  - Fetch shopping items on mount
  - Display items grouped by completed/incomplete
- [ ] **Shopping Item Component**
  - Checkbox to mark complete/incomplete
  - Display description
  - Edit button (inline edit)
  - Delete button with confirmation
- [ ] **Clear Completed Button**
  - Bulk delete all completed items

#### 2.6 Calendar Page
- [ ] **Zustand Store for Calendar Events**
  - State: calendar_events array, loading, error
  - Actions: fetchEvents, updateEvent, deleteEvent
- [ ] **Calendar View Component**
  - List view of events sorted by date/time
  - Group by date
  - Display event description, date, time
- [ ] **Event Item Component**
  - Display event details
  - Edit button (inline or modal)
  - Delete button with confirmation

---

### Phase 3: UI Polish & User Experience

#### 3.1 Styling
- [ ] Choose CSS framework or styling approach (Tailwind, Material-UI, styled-components)
- [ ] Design system: colors, typography, spacing
- [ ] Responsive design for mobile/tablet/desktop
- [ ] Loading spinners and skeletons
- [ ] Error message styling
- [ ] Empty states (no tasks, no shopping items, etc.)

#### 3.2 User Feedback
- [ ] Toast notifications for success/error
- [ ] Confirmation modals for destructive actions
- [ ] Loading states for all async operations
- [ ] Form validation with error messages

#### 3.3 Accessibility
- [ ] Keyboard navigation
- [ ] ARIA labels
- [ ] Focus management
- [ ] Screen reader support

---

### Phase 4: Testing & Deployment Prep

#### 4.1 Testing
- [ ] Backend endpoint tests (pytest)
- [ ] Frontend component tests (Jest/Vitest)
- [ ] Integration tests for critical flows
- [ ] Manual E2E testing checklist

#### 4.2 Deployment
- [ ] Backend deployment setup (Render, Railway, or similar)
- [ ] Frontend deployment setup (Vercel, Netlify, or similar)
- [ ] Environment variable configuration
- [ ] Database migrations in production
- [ ] CORS configuration for production URLs

---

## Future Enhancements (Post-MVP)

### Authentication
- [ ] Google OAuth integration
- [ ] Password-based authentication option
- [ ] "Remember me" functionality
- [ ] Password reset flow

### Features
- [ ] Task categories/tags
- [ ] Calendar integration (Google Calendar sync)
- [ ] Recurring tasks
- [ ] Task prioritization
- [ ] Search functionality
- [ ] Filtering by date ranges
- [ ] Export data (CSV, JSON)
- [ ] Sharing/collaboration features
- [ ] Notifications/reminders
- [ ] Dark mode

### Technical Improvements
- [ ] API rate limiting
- [ ] Caching layer
- [ ] Database indexing optimization
- [ ] Logging and monitoring
- [ ] Error tracking (Sentry)
- [ ] Analytics

---

## Estimated Timeline

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1: Backend API Completion | 15 tasks | 2-3 days |
| Phase 2: Frontend Pages & Components | 25 tasks | 5-7 days |
| Phase 3: UI Polish & UX | 10 tasks | 2-3 days |
| Phase 4: Testing & Deployment | 8 tasks | 1-2 days |
| **Total** | **58 tasks** | **10-15 days** |

---

## Success Criteria

The MVP is complete when:
1. ✅ Users can log in with email
2. ✅ Users can create brain dumps and see categorized results
3. ✅ Users can view their tasks, shopping items, and calendar events in separate tabs
4. ✅ Users can mark items as complete
5. ✅ Users can edit and delete items
6. ✅ The app is deployed and accessible via URL
7. ✅ Basic error handling and loading states work correctly

---

## Priority Order for Implementation

### Week 1: Core Backend + Basic Frontend
1. Backend GET/UPDATE/DELETE endpoints
2. Login page
3. Main layout with tabs
4. Home page (brain dump form)

### Week 2: Feature Pages
5. Tasks page with CRUD
6. Shopping page with CRUD
7. Calendar page with CRUD
8. Basic styling

### Week 3: Polish & Deploy
9. UI polish and responsive design
10. Testing
11. Deployment
