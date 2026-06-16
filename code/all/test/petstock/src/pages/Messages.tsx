import { useEffect, useState } from 'react';
import { collection, query, where, onSnapshot, getDoc, doc } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';
import { handleFirestoreError, OperationType } from '../lib/errorHandling';
import { formatDistanceToNow } from 'date-fns';
import { UserProfile } from '../lib/types';
import { MessageSquare } from 'lucide-react';

interface ChatPreview {
    id: string;
    updatedAt: number | any;
    listingId: string;
    otherUser: UserProfile | null;
}

export default function Messages() {
    const { user } = useAuth();
    const [chats, setChats] = useState<ChatPreview[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!user) return;

        const q = query(collection(db, 'chats'), where('participantIds', 'array-contains', user.uid));
        
        const unsubscribe = onSnapshot(q, async (snapshot) => {
            try {
                const chatPromises = snapshot.docs.map(async (chatDoc) => {
                    const data = chatDoc.data();
                    const otherUserId = data.participantIds.find((id: string) => id !== user.uid);
                    
                    let otherUser = null;
                    if (otherUserId) {
                        const userSnap = await getDoc(doc(db, 'users', otherUserId));
                        if (userSnap.exists()) {
                            otherUser = { id: userSnap.id, ...userSnap.data() } as UserProfile;
                        }
                    }

                    return {
                        id: chatDoc.id,
                        updatedAt: data.updatedAt,
                        listingId: data.listingId,
                        otherUser
                    } as ChatPreview;
                });

                const resolvedChats = await Promise.all(chatPromises);
                resolvedChats.sort((a, b) => {
                    const timeA = a.updatedAt?.toMillis?.() || a.updatedAt || 0;
                    const timeB = b.updatedAt?.toMillis?.() || b.updatedAt || 0;
                    return timeB - timeA;
                });
                
                setChats(resolvedChats);
            } catch (error) {
                console.error("Error processing chats:", error);
            } finally {
                setLoading(false);
            }
        }, (error) => {
             handleFirestoreError(error, OperationType.LIST, 'chats');
        });

        return () => unsubscribe();
    }, [user]);

    if (loading) {
        return <div className="p-8 text-center text-slate-500">Loading chats...</div>;
    }

    return (
        <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-8">Messages</h1>
            
            {chats.length === 0 ? (
                <div className="text-center py-20 bg-white rounded-3xl border border-slate-100">
                    <MessageSquare className="w-12 h-12 text-slate-300 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-slate-900">No messages yet</h3>
                    <p className="mt-1 text-slate-500">Contact a seller or wait for buyers to message you.</p>
                </div>
            ) : (
                <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden text-left divide-y divide-slate-100">
                    {chats.map(chat => (
                        <Link key={chat.id} to={`/chat/${chat.id}`} className="block p-4 hover:bg-slate-50 transition-colors">
                            <div className="flex items-center gap-4">
                                <img 
                                    src={chat.otherUser?.photoURL || 'https://ui-avatars.com/api/?name=' + (chat.otherUser?.displayName || 'User')} 
                                    alt="User" 
                                    className="w-12 h-12 rounded-full border border-slate-200"
                                    referrerPolicy="no-referrer"
                                />
                                <div className="flex-1 min-w-0">
                                    <div className="flex justify-between items-baseline mb-1">
                                        <h3 className="text-base font-semibold text-slate-900 truncate">
                                            {chat.otherUser?.displayName || 'Anonymous'}
                                        </h3>
                                        {chat.updatedAt && (
                                            <span className="text-xs text-slate-400">
                                                {formatDistanceToNow(chat.updatedAt?.toMillis?.() || chat.updatedAt || Date.now(), { addSuffix: true })}
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-sm text-slate-500 truncate">
                                        Chat regarding listing ID: {chat.listingId}
                                    </p>
                                </div>
                            </div>
                        </Link>
                    ))}
                </div>
            )}
        </div>
    );
}
