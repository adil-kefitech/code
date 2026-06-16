import { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { doc, getDoc, collection, addDoc, query, where, getDocs, serverTimestamp } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { Listing, UserProfile } from '../lib/types';
import { useAuth } from '../contexts/AuthContext';
import { MapPin, Clock, Info, ShieldCheck, Heart, Share2, MessageSquare } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { handleFirestoreError, OperationType } from '../lib/errorHandling';

export default function ListingView() {
  const { id } = useParams<{ id: string }>();
  const [listing, setListing] = useState<Listing | null>(null);
  const [seller, setSeller] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchListing() {
      if (!id) return;
      try {
        const docRef = doc(db, 'listings', id);
        const docSnap = await getDoc(docRef);
        
        if (docSnap.exists()) {
          const data = docSnap.data() as Listing;
          setListing({ id: docSnap.id, ...data });
          
          if (data.sellerId) {
            const userRef = doc(db, 'users', data.sellerId);
            const userSnap = await getDoc(userRef);
            if (userSnap.exists()) {
                setSeller({ id: userSnap.id, ...userSnap.data() } as UserProfile);
            }
          }
        }
      } catch (error) {
         handleFirestoreError(error, OperationType.GET, `listings/${id}`);
      } finally {
        setLoading(false);
      }
    }
    fetchListing();
  }, [id]);

  const handleContactSeller = async () => {
    if (!user) {
        // Maybe open login modal or redirect to login (if we had one)
        alert('Please login to contact the seller.');
        return;
    }
    if (user.uid === listing?.sellerId) {
        alert('You cannot message yourself.');
        return;
    }

    try {
        // Check if chat already exists
        const q = query(
            collection(db, 'chats'), 
            where('participantIds', 'array-contains', user.uid),
            where('listingId', '==', listing?.id)
        );
        const querySnapshot = await getDocs(q);
        
        let chatId = null;
        querySnapshot.forEach((doc) => {
            const data = doc.data();
            if (data.participantIds.includes(listing?.sellerId)) {
                chatId = doc.id;
            }
        });

        if (chatId) {
            navigate(`/chat/${chatId}`);
        } else {
            // Create new chat
            const newChatRef = await addDoc(collection(db, 'chats'), {
                participantIds: [user.uid, listing?.sellerId],
                listingId: listing?.id,
                updatedAt: serverTimestamp()
            });
            navigate(`/chat/${newChatRef.id}`);
        }
    } catch (error) {
        handleFirestoreError(error, OperationType.CREATE, 'chats');
    }
  };

  if (loading) {
      return (
          <div className="flex justify-center py-32">
              <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          </div>
      );
  }

  if (!listing) {
      return (
          <div className="text-center py-32">
              <h2 className="text-2xl font-bold text-slate-900">Listing not found</h2>
              <Link to="/" className="text-indigo-600 font-medium hover:underline mt-4 inline-block">Go back home</Link>
          </div>
      );
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8 pb-24 md:pb-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Main Content: Images and Details */}
          <div className="lg:col-span-2 space-y-6">
             <div className="bg-white rounded-3xl overflow-hidden shadow-sm border border-slate-100 aspect-[4/3] sm:aspect-[16/9] relative">
                {listing.images && listing.images.length > 0 ? (
                    <img src={listing.images[0]} alt={listing.title} className="w-full h-full object-cover" />
                ) : (
                    <div className="w-full h-full flex items-center justify-center bg-slate-100 text-slate-400">
                        <span className="text-6xl">🐾</span>
                    </div>
                )}
             </div>

             <div className="bg-white p-6 sm:p-8 rounded-3xl shadow-sm border border-slate-100">
                 <div className="flex flex-wrap items-start justify-between gap-4 mb-6">
                     <div>
                         <div className="inline-flex items-center rounded-full bg-indigo-50 px-2.5 py-0.5 text-xs font-semibold text-indigo-600 mb-3">
                             {listing.category}
                         </div>
                         <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900">{listing.title}</h1>
                         <div className="flex items-center gap-4 text-sm text-slate-500 mt-3 font-medium">
                            <span className="flex items-center gap-1"><MapPin className="w-4 h-4" /> {listing.location}</span>
                            <span className="flex items-center gap-1"><Clock className="w-4 h-4" /> {listing.createdAt ? formatDistanceToNow(typeof listing.createdAt === 'number' ? listing.createdAt : listing.createdAt?.toMillis?.() || Date.now(), { addSuffix: true }) : 'Just now'}</span>
                         </div>
                     </div>
                     <div className="flex gap-2">
                         <button className="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-red-500 transition-colors">
                             <Heart className="w-5 h-5" />
                         </button>
                         <button className="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 text-slate-600 hover:bg-slate-50 hover:text-indigo-600 transition-colors">
                             <Share2 className="w-5 h-5" />
                         </button>
                     </div>
                 </div>

                 {/* Key Attributes */}
                 <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 py-6 border-y border-slate-100 mb-6">
                    <div className="flex flex-col">
                        <span className="text-sm text-slate-500 mb-1">Breed</span>
                        <span className="font-semibold text-slate-900">{listing.breed || 'Not specified'}</span>
                    </div>
                    <div className="flex flex-col">
                        <span className="text-sm text-slate-500 mb-1">Age</span>
                        <span className="font-semibold text-slate-900">{listing.age || 'Not specified'}</span>
                    </div>
                 </div>

                 <div className="space-y-4">
                     <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                         <Info className="w-5 h-5 text-indigo-600" /> Description
                     </h2>
                     <p className="text-slate-600 text-base leading-relaxed whitespace-pre-line">
                         {listing.description}
                     </p>
                 </div>
             </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
              <div className="bg-white p-6 rounded-3xl shadow-lg border border-slate-100 sticky top-24">
                  <div className="mb-6">
                    <p className="text-sm text-slate-500 font-medium mb-1">Price</p>
                    <p className="text-5xl font-extrabold text-slate-900">${listing.price.toLocaleString()}</p>
                  </div>

                  <button 
                    onClick={handleContactSeller}
                    disabled={user?.uid === listing.sellerId}
                    className="w-full flex items-center justify-center gap-2 py-4 px-4 border border-transparent rounded-2xl shadow-sm text-base font-bold text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed mb-4"
                  >
                      <MessageSquare className="w-5 h-5" />
                      {user?.uid === listing.sellerId ? 'This is your listing' : 'Contact Seller'}
                  </button>

                  <div className="p-4 bg-slate-50 rounded-2xl mb-6">
                      <h3 className="font-semibold text-slate-900 mb-3 text-sm uppercase tracking-wider text-center">About the Seller</h3>
                      <div className="flex flex-col items-center text-center">
                          <img 
                            src={seller?.photoURL || 'https://ui-avatars.com/api/?name=' + (seller?.displayName || 'User')} 
                            alt={seller?.displayName || 'Seller'} 
                            className="w-16 h-16 rounded-full border-4 border-white shadow-sm mb-3"
                            referrerPolicy="no-referrer"
                          />
                          <p className="font-bold text-lg text-slate-900">{seller?.displayName || 'Anonymous User'}</p>
                          <p className="text-sm text-slate-500 mt-1 flex items-center gap-1 justify-center"><ShieldCheck className="w-4 h-4 text-emerald-500" /> Verified Member</p>
                      </div>
                  </div>

                  {/* Safety Tips */}
                  <div className="text-xs text-slate-500 space-y-2 border-t pt-4">
                      <p className="font-bold text-slate-700 flex items-center gap-1"><ShieldCheck className="w-3 h-3 text-emerald-500 mt-0.5" /> Safety Tips</p>
                      <ul className="list-disc pl-4 space-y-1">
                          <li>Meet in a public place.</li>
                          <li>Never send money before seeing the pet.</li>
                          <li>Ask for health records and details.</li>
                      </ul>
                  </div>
              </div>
          </div>

      </div>
    </div>
  );
}
