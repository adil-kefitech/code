import React, { useEffect, useState, useRef } from 'react';
import { useParams, Navigate, Link } from 'react-router-dom';
import { doc, getDoc, collection, query, orderBy, onSnapshot, addDoc, serverTimestamp } from 'firebase/firestore';
import { db } from '../lib/firebase';
import { Chat, Message, UserProfile } from '../lib/types';
import { useAuth } from '../contexts/AuthContext';
import { handleFirestoreError, OperationType } from '../lib/errorHandling';
import { ArrowLeft, Send } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export default function ChatView() {
  const { id } = useParams<{ id: string }>();
  const { user } = useAuth();
  const [chat, setChat] = useState<Chat | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [otherUser, setOtherUser] = useState<UserProfile | null>(null);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (!id || !user) return;

    // Fetch Chat metadata and other user
    const fetchChatData = async () => {
      try {
        const chatRef = doc(db, 'chats', id);
        const chatSnap = await getDoc(chatRef);
        if (chatSnap.exists()) {
          const chatData = { id: chatSnap.id, ...chatSnap.data() } as Chat;
          setChat(chatData);

          const otherUserId = chatData.participantIds.find(pId => pId !== user.uid);
          if (otherUserId) {
              const otherUserSnap = await getDoc(doc(db, 'users', otherUserId));
              if (otherUserSnap.exists()) setOtherUser(otherUserSnap.data() as UserProfile);
          }
        }
      } catch (error) {
        handleFirestoreError(error, OperationType.GET, `chats/${id}`);
      }
    };

    fetchChatData();

    // Listen for messages
    const messagesQuery = query(
      collection(db, 'chats', id, 'messages'),
      orderBy('createdAt', 'asc')
    );
    
    const unsubscribe = onSnapshot(messagesQuery, (snapshot) => {
      const fetchedMessages = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      })) as Message[];
      setMessages(fetchedMessages);
      setLoading(false);
    }, (error) => {
      handleFirestoreError(error, OperationType.GET, `chats/${id}/messages`);
      setLoading(false);
    });

    return unsubscribe;
  }, [id, user]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMessage.trim() || !id || !user) return;

    const messageText = newMessage.trim();
    setNewMessage('');

    try {
      await addDoc(collection(db, 'chats', id, 'messages'), {
        senderId: user.uid,
        text: messageText,
        createdAt: serverTimestamp()
      });
    } catch (error) {
      handleFirestoreError(error, OperationType.CREATE, `chats/${id}/messages`);
      setNewMessage(messageText); // restore on error
    }
  };

  if (!user) return <Navigate to="/" replace />;
  
  if (loading) return (
      <div className="flex h-screen items-center justify-center">
          <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent inset-0 rounded-full animate-spin"></div>
      </div>
  );

  if (!chat) return <div className="p-8 text-center">Chat not found</div>;

  return (
    <div className="mx-auto max-w-4xl px-4 py-6 sm:px-6 h-[calc(100vh-64px)] flex flex-col">
      <div className="bg-white border text-slate-900 rounded-t-2xl shadow-sm px-6 py-4 flex items-center gap-4">
          <Link to="/" className="p-2 hover:bg-slate-100 rounded-full text-slate-500 transition-colors">
              <ArrowLeft className="w-5 h-5" />
          </Link>
          <img 
            src={otherUser?.photoURL || 'https://ui-avatars.com/api/?name=' + (otherUser?.displayName || 'User')} 
            alt={otherUser?.displayName || 'User'} 
            className="w-10 h-10 rounded-full"
            referrerPolicy="no-referrer"
          />
          <div>
              <h2 className="font-bold text-lg">{otherUser?.displayName || 'Unknown User'}</h2>
          </div>
      </div>
      
      <div className="flex-1 bg-slate-50 border-x overflow-y-auto p-4 sm:p-6 flex flex-col gap-4">
        {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center text-slate-400">
                Send a message to start the conversation!
            </div>
        ) : (
            messages.map((msg) => {
                const isMine = msg.senderId === user.uid;
                return (
                    <div key={msg.id} className={`flex ${isMine ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[75%] rounded-2xl px-5 py-3 ${isMine ? 'bg-indigo-600 text-white rounded-tr-sm shadow-sm' : 'bg-white border text-slate-800 rounded-tl-sm shadow-sm'}`}>
                            <p className="whitespace-pre-wrap">{msg.text}</p>
                            {msg.createdAt && (
                                <p className={`text-[10px] mt-1 text-right ${isMine ? 'text-indigo-200' : 'text-slate-400'}`}>
                                    {typeof msg.createdAt === 'number' ? formatDistanceToNow(msg.createdAt) + ' ago' : formatDistanceToNow(msg.createdAt?.toMillis?.() || Date.now()) + ' ago'}
                                </p>
                            )}
                        </div>
                    </div>
                );
            })
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="bg-white border rounded-b-2xl shadow-sm p-4">
          <form onSubmit={handleSendMessage} className="flex gap-2">
              <input 
                  type="text" 
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Type a message..."
                  className="flex-1 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
              <button 
                type="submit" 
                disabled={!newMessage.trim()}
                className="bg-indigo-600 hover:bg-indigo-700 text-white p-3 rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center aspect-square"
              >
                  <Send className="w-5 h-5" />
              </button>
          </form>
      </div>
    </div>
  );
}
