import React, { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { db } from '../lib/firebase';
import { collection, doc, setDoc, serverTimestamp } from 'firebase/firestore';
import { handleFirestoreError, OperationType } from '../lib/errorHandling';

export default function Sell() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: '',
    category: 'Dog',
    breed: '',
    age: '',
    location: '',
    imageUrl: '',
  });

  if (!user) {
    return <Navigate to="/" replace />;
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
        const listingId = doc(collection(db, 'listings')).id;
        const newListing = {
            title: formData.title,
            description: formData.description,
            price: Number(formData.price),
            category: formData.category,
            breed: formData.breed,
            age: formData.age,
            location: formData.location,
            images: formData.imageUrl ? [formData.imageUrl] : [],
            sellerId: user.uid,
            status: 'active',
            createdAt: serverTimestamp(),
            updatedAt: serverTimestamp(),
        };

        await setDoc(doc(db, 'listings', listingId), newListing);
        navigate(`/listing/${listingId}`);
    } catch (err: unknown) {
        try {
           handleFirestoreError(err, OperationType.CREATE, 'listings');
        } catch (fhErr: any) {
           setError(fhErr.message);
        }
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6 lg:px-8 bg-white my-8 rounded-2xl shadow-sm border border-slate-100">
      <h1 className="text-3xl font-bold tracking-tight text-slate-900 mb-2">Post an Ad</h1>
      <p className="mt-2 text-slate-500 mb-8 border-b pb-4">Fill in the details about the pet you are selling.</p>
      
      {error && (
        <div className="mb-6 p-4 rounded-lg bg-red-50 text-red-600 text-sm">
            {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-slate-700">Ad Title*</label>
          <input required type="text" name="title" id="title" value={formData.title} onChange={handleChange} className="mt-1 block w-full rounded-xl border-slate-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-3 border" placeholder="e.g., Golden Retriever Puppy" />
        </div>

        <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-slate-700">Category*</label>
              <select required name="category" id="category" value={formData.category} onChange={handleChange} className="mt-1 block w-full rounded-xl border-slate-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-3 border bg-white">
                <option value="Dog">Dog</option>
                <option value="Cat">Cat</option>
                <option value="Bird">Bird</option>
                <option value="Fish">Fish</option>
                <option value="Rabbit">Rabbit</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label htmlFor="price" className="block text-sm font-medium text-slate-700">Price ($)*</label>
              <input required type="number" name="price" id="price" min="0" value={formData.price} onChange={handleChange} className="mt-1 block w-full rounded-xl border-slate-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-3 border" placeholder="0.00" />
            </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="breed" className="block text-sm font-medium text-slate-700">Breed</label>
              <input type="text" name="breed" id="breed" value={formData.breed} onChange={handleChange} className="mt-1 block w-full rounded-xl border-slate-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-3 border" placeholder="e.g., Golden Retriever" />
            </div>
            <div>
              <label htmlFor="age" className="block text-sm font-medium text-slate-700">Age</label>
              <input type="text" name="age" id="age" value={formData.age} onChange={handleChange} className="mt-1 block w-full rounded-xl border-slate-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-3 border" placeholder="e.g., 2 months" />
            </div>
        </div>

        <div>
          <label htmlFor="location" className="block text-sm font-medium text-slate-700">Location*</label>
          <input required type="text" name="location" id="location" value={formData.location} onChange={handleChange} className="mt-1 block w-full rounded-xl border-slate-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-3 border" placeholder="e.g., New York, NY" />
        </div>

        <div>
          <label htmlFor="imageUrl" className="block text-sm font-medium text-slate-700">Image URL</label>
          <input type="url" name="imageUrl" id="imageUrl" value={formData.imageUrl} onChange={handleChange} className="mt-1 block w-full rounded-xl border-slate-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-3 border" placeholder="https://example.com/pet.jpg" />
        </div>

        <div>
          <label htmlFor="description" className="block text-sm font-medium text-slate-700">Description*</label>
          <textarea required name="description" id="description" rows={5} value={formData.description} onChange={handleChange} className="mt-1 block w-full rounded-xl border-slate-200 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm px-4 py-3 border" placeholder="Describe the pet..."></textarea>
        </div>

        <button disabled={loading} type="submit" className="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-colors">
          {loading ? 'Posting...' : 'Post Ad'}
        </button>
      </form>
    </div>
  );
}
