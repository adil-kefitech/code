import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Settings, MessageSquare, PlusCircle, User as UserIcon, LogOut, Home, Search, Heart } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { auth } from '../lib/firebase';
import { signInWithPopup, GoogleAuthProvider, signOut } from 'firebase/auth';

function MainNavigation() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const provider = new GoogleAuthProvider();
      await signInWithPopup(auth, provider);
    } catch (error) {
      console.error('Error signing in:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white shadow-lg">
            <span className="text-xl font-bold">P</span>
          </div>
          <span className="hidden text-xl font-bold tracking-tight text-slate-900 sm:block">Petstock</span>
        </Link>

        {/* Desktop Navigation */}
        <div className="hidden flex-1 items-center justify-end gap-6 md:flex">
          {user ? (
            <>
              <Link to="/messages" className="text-slate-500 hover:text-slate-900 transition-colors">
                <MessageSquare className="h-5 w-5" />
              </Link>
              <Link to="/sell" className="flex items-center gap-2 rounded-full bg-slate-900 px-5 py-2.5 text-sm font-medium text-white transition-all hover:bg-slate-800 hover:shadow-md hover:-translate-y-0.5">
                <PlusCircle className="h-4 w-4" />
                <span>Sell Pet</span>
              </Link>
              <div className="group relative">
                <button className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-100 text-slate-600 hover:bg-slate-200 hover:text-slate-900 transition-colors">
                  {user.photoURL ? (
                    <img src={user.photoURL} alt={user.displayName || 'User'} className="h-full w-full rounded-full object-cover" referrerPolicy="no-referrer" />
                  ) : (
                    <UserIcon className="h-5 w-5" />
                  )}
                </button>
                <div className="absolute right-0 mt-2 hidden w-48 rounded-xl border bg-white p-2 shadow-lg group-hover:block">
                  <div className="px-3 py-2 border-b mb-2">
                    <p className="text-sm font-medium truncate">{user.displayName}</p>
                    <p className="text-xs text-slate-500 truncate">{user.email}</p>
                  </div>
                  <Link to="/profile" className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm text-slate-600 hover:bg-slate-50 hover:text-slate-900">
                    <UserIcon className="h-4 w-4" /> Profile
                  </Link>
                  <button onClick={handleLogout} className="flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm text-red-600 hover:bg-red-50">
                    <LogOut className="h-4 w-4" /> Logout
                  </button>
                </div>
              </div>
            </>
          ) : (
            <>
              <button onClick={handleLogin} className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors">Log In</button>
              <button onClick={handleLogin} className="rounded-full bg-slate-900 px-5 py-2.5 text-sm font-medium text-white transition-all hover:bg-slate-800 hover:shadow-md">Sign Up</button>
              <button 
                onClick={handleLogin}
                className="flex items-center gap-2 rounded-full bg-indigo-50 px-5 py-2.5 text-sm font-medium text-indigo-600 transition-all hover:bg-indigo-100"
              >
                <PlusCircle className="h-4 w-4" />
                <span>Sell</span>
              </button>
            </>
          )}
        </div>
      </div>

      {/* Mobile Bottom Navigation */}
      <div className="fixed bottom-0 left-0 z-50 flex w-full justify-around border-t bg-white pb-safe pt-2 sm:hidden shadow-[0_-4px_20px_-10px_rgba(0,0,0,0.1)]">
        <Link to="/" className="flex flex-col items-center gap-1 p-2 text-slate-500 hover:text-indigo-600">
          <Home className="h-5 w-5" />
          <span className="text-[10px] font-medium">Home</span>
        </Link>
        <Link to="/search" className="flex flex-col items-center gap-1 p-2 text-slate-500 hover:text-indigo-600">
          <Search className="h-5 w-5" />
          <span className="text-[10px] font-medium">Search</span>
        </Link>
        <Link to="/sell" className="relative -top-5 flex h-12 w-12 items-center justify-center rounded-full bg-indigo-600 text-white shadow-lg ring-4 ring-white transition-transform hover:scale-105">
          <PlusCircle className="h-6 w-6" />
        </Link>
        <Link to="/messages" className="flex flex-col items-center gap-1 p-2 text-slate-500 hover:text-indigo-600">
          <MessageSquare className="h-5 w-5" />
          <span className="text-[10px] font-medium">Chat</span>
        </Link>
        <Link to="/profile" className="flex flex-col items-center gap-1 p-2 text-slate-500 hover:text-indigo-600">
          <UserIcon className="h-5 w-5" />
          <span className="text-[10px] font-medium">Profile</span>
        </Link>
      </div>
    </nav>
  );
}

export default MainNavigation;
