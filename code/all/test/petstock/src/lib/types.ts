export interface UserProfile {
  id: string; // Document ID
  email: string | null;
  displayName: string | null;
  photoURL: string | null;
  createdAt: number;
}

export interface Listing {
  id: string; // Document ID
  title: string;
  description: string;
  price: number;
  category: string;
  breed?: string;
  age?: string;
  location: string;
  images: string[];
  sellerId: string;
  status: 'active' | 'sold' | 'archived';
  createdAt: number;
  updatedAt: number;
}

export interface SavedListing {
  id: string;
  userId: string;
  listingId: string;
  createdAt: number;
}

export interface Chat {
  id: string; // Document ID
  participantIds: string[];
  listingId: string;
  updatedAt: number;
}

export interface Message {
  id: string; // Document ID
  senderId: string;
  text: string;
  createdAt: number;
}

