import { useEffect, useState } from 'react';
import { collection, query, orderBy, limit, getDocs } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { Listing } from '../lib/types';
import { formatCurrency } from '../lib/helpers';
import { MapPin, Clock } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { Link } from 'react-router-dom';
import { handleFirestoreError, OperationType } from '../lib/errorHandling';

export default function Home() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchListings() {
      try {
        const q = query(
          collection(db, 'listings'),
          orderBy('createdAt', 'desc'),
          limit(20)
        );
        const snapshot = await getDocs(q);
        const fetchedListings = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        })) as Listing[];
        setListings(fetchedListings);
      } catch (error) {
        handleFirestoreError(error, OperationType.LIST, 'listings');
      } finally {
        setLoading(false);
      }
    }
    fetchListings();
  }, []);

  const getCreatedAt = (listing: Listing) => {
     if (!listing.createdAt) return Date.now();
     if (typeof listing.createdAt === 'number') return listing.createdAt;
     if (typeof (listing.createdAt as any).toMillis === 'function') return (listing.createdAt as any).toMillis();
     return Date.now();
  };

  return (
    <div className="flex-1 bg-slate-50 min-h-screen pb-20 md:pb-0">
      {/* Hero Section */}
      <div className="bg-indigo-600 px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl lg:text-6xl max-w-2xl">
            Find your perfect companion.
          </h1>
          <p className="mt-4 text-xl text-indigo-100 max-w-xl">
            Discover thousands of pets waiting for a loving home locally and safely on Petstock.
          </p>
          <div className="mt-10 flex gap-4 max-w-xl bg-white p-2 rounded-xl shadow-lg">
             <input type="text" placeholder="Search 'Golden Retriever'..." className="flex-1 border-0 bg-transparent px-4 py-3 text-slate-900 focus:ring-0 outline-none" />
             <button className="bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition">Search</button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold tracking-tight text-slate-900 mb-8">Fresh Recommendations</h2>
        
        {loading ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="animate-pulse rounded-2xl bg-white p-4 shadow-sm">
                <div className="aspect-square w-full rounded-xl bg-slate-200"></div>
                <div className="mt-4 h-6 w-2/3 rounded-lg bg-slate-200"></div>
                <div className="mt-2 h-4 w-1/3 rounded-lg bg-slate-200"></div>
              </div>
            ))}
          </div>
        ) : listings.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {listings.map((listing) => (
              <Link key={listing.id} to={`/listing/${listing.id}`} className="group relative rounded-2xl bg-white p-4 shadow-sm transition-all hover:shadow-xl hover:-translate-y-1 block border border-transparent hover:border-indigo-100">
                <div className="aspect-[4/3] w-full overflow-hidden rounded-xl bg-slate-100 relative">
                  {listing.images && listing.images.length > 0 ? (
                    <img 
                      src={listing.images[0]} 
                      alt={listing.title} 
                      className="h-full w-full object-cover transition-transform group-hover:scale-105"
                    />
                  ) : (
                    <div className="h-full w-full flex items-center justify-center text-slate-400">No Image</div>
                  )}
                  {listing.status === 'sold' && (
                    <div className="absolute top-2 right-2 bg-slate-900/80 backdrop-blur text-white text-xs font-bold px-2 py-1 rounded">
                      SOLD
                    </div>
                  )}
                </div>
                <div className="mt-4 flex items-start justify-between gap-4">
                  <div>
                    <h3 className="text-lg font-semibold text-slate-900 line-clamp-1">{formatCurrency(listing.price)}</h3>
                    <p className="mt-1 text-sm font-medium text-slate-500 line-clamp-2">{listing.title}</p>
                  </div>
                </div>
                <div className="mt-4 flex items-center gap-4 text-xs text-slate-400">
                  <div className="flex items-center gap-1 min-w-0">
                    <MapPin className="h-3 w-3 shrink-0" />
                    <span className="truncate">{listing.location}</span>
                  </div>
                  <div className="flex items-center gap-1 shrink-0">
                    <Clock className="h-3 w-3" />
                    <span>{formatDistanceToNow(getCreatedAt(listing))} ago</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-20 bg-white rounded-3xl border border-dashed border-slate-300">
            <h3 className="text-lg font-medium text-slate-900">No listings yet</h3>
            <p className="mt-1 text-slate-500">Be the first to post a pet for sale!</p>
            <Link to="/sell" className="mt-6 inline-flex items-center rounded-full bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500">
              Post an Ad
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
