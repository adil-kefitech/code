import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navigation from './components/Navigation';
import Home from './pages/Home';
import Sell from './pages/Sell';
import ListingView from './pages/ListingView';
import ChatView from './pages/Chat';
import Messages from './pages/Messages';
import Profile from './pages/Profile';

export default function App() {
  return (
    <AuthProvider>
      <div className="flex min-h-screen flex-col font-sans text-slate-900 selection:bg-indigo-100 selection:text-indigo-900">
        <Navigation />
        <main className="flex-1 bg-slate-50">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/sell" element={<Sell />} />
            <Route path="/listing/:id" element={<ListingView />} />
            <Route path="/chat/:id" element={<ChatView />} />
            <Route path="/messages" element={<Messages />} />
            <Route path="/profile" element={<Profile />} />
            {/* Catch-all */}
            <Route path="*" element={<Home />} />
          </Routes>
        </main>
      </div>
    </AuthProvider>
  );
}
