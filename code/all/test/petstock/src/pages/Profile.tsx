import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Navigate, Link } from 'react-router-dom';
import { collection, query, where, getDocs, doc, deleteDoc } from 'firebase/firestore';
import { db, auth } from '../lib/firebase';
import { Listing } from '../lib/types';
import { handleFirestoreError, OperationType } from '../lib/errorHandling';
import { formatCurrency } from '../lib/helpers';
import { Trash2, Edit2, LogOut } from 'lucide-react';
import { signOut } from 'firebase/auth';

export default function Profile() {
  const { user } = useAuth();
  const [myListings, setMyListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    const fetchMyListings = async () => {
      try {
        const q = query(collection(db, 'listings'), where('sellerId', '==', user.uid));
        const snapshot = await getDocs(q);
        const data = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })) as Listing[];
        setMyListings(data);
      } catch (error) {
        handleFirestoreError(error, OperationType.LIST, 'listings');
      } finally {
        setLoading(false);
      }
    };
    fetchMyListings();
  }, [user]);

  if (!user) return <Navigate to="/" replace />;

  const handleDelete = async (listingId: string) => {
    if (!window.confirm('Are you sure you want to delete this listing?')) return;
    try {
      await deleteDoc(doc(db, 'listings', listingId));
      setMyListings(myListings.filter(l => l.id !== listingId));
    } catch (error) {
      handleFirestoreError(error, OperationType.DELETE, `listings/${listingId}`);
    }
  };

  const handleSignOut = () => {
    signOut(auth);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="bg-white rounded-3xl p-8 mb-8 shadow-sm flex items-center justify-between">
          <div className="flex items-center gap-6">
              <img 
                  src={user.photoURL || `https://ui-avatars.com/api/?name=${user.displayName}`} 
                  alt={user.displayName || 'Profile'} 
                  className="w-24 h-24 rounded-full shadow-md border-4 border-white"
                  referrerPolicy="no-referrer"
              />
              <div>
                  <h1 className="text-3xl font-bold text-slate-900">{user.displayName}</h1>
                  <p className="text-slate-500 mt-1">{user.email}</p>
              </div>
          </div>
          <button onClick={handleSignOut} className="text-red-500 hover:bg-red-50 px-4 py-2 rounded-xl transition flex items-center gap-2 font-medium">
             <LogOut className="w-5 h-5" /> Sign Out
          </button>
      </div>

      <h2 className="text-2xl font-bold tracking-tight text-slate-900 mb-6">My Listings</h2>
      
      {loading ? (
          <div className="text-center py-20">Loading...</div>
      ) : myListings.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-slate-300">
             <p className="text-slate-500">You haven't posted any listings yet.</p>
             <Link to="/sell" className="mt-4 inline-block text-indigo-600 font-medium">Post your first ad</Link>
          </div>
      ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {myListings.map(listing => (
                  <div key={listing.id} className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden flex flex-col">
                      <div className="aspect-[4/3] bg-slate-100 relative">
                          {listing.images && listing.images.length > 0 ? (
                               <img src={listing.images[0]} alt={listing.title} className="w-full h-full object-cover" />
                          ) : (
                               <div className="w-full h-full flex items-center justify-center text-slate-400">No Image</div>
                          )}
                          <div className="absolute top-2 right-2 bg-white/90 backdrop-blur px-2 py-1 rounded text-xs font-bold shadow-sm select-none">
                              {listing.status.toUpperCase()}
                          </div>
                      </div>
                      <div className="p-4 flex-1">
                          <h3 className="font-semibold text-lg text-slate-900 line-clamp-1">{listing.title}</h3>
                          <p className="font-bold text-indigo-600 mt-1">{formatCurrency(listing.price)}</p>
                      </div>
                      <div className="px-4 py-3 bg-slate-50 border-t border-slate-100 flex justify-end gap-2">
                          <button onClick={() => handleDelete(listing.id)} className="p-2 text-red-500 hover:bg-red-100 rounded-lg transition-colors">
                              <Trash2 className="w-5 h-5" />
                          </button>
                          <Link to={`/listing/${listing.id}`} className="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition">
                             View
                          </Link>
                      </div>
                  </div>
              ))}
          </div>
      )}
    </div>
  );
}
