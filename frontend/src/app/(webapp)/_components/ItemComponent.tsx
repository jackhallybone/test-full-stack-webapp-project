'use client';  // Ensures this component is client-side rendered

import { useEffect } from 'react';
import { useUpdateItem } from './useUpdateItem'; // Custom hook for mutation

const ItemComponent = ({ item }) => {
    // Use the custom hook for update logic
    const {
        savedItem,
        liveItem,
        status,
        handleChange,
        handleSubmit
    } = useUpdateItem(item);

    useEffect(() => {
        // Reset saved and live state when item prop changes
        savedItem.name = item.name || '';
        savedItem.description = item.description || '';
        liveItem.name = item.name || '';
        liveItem.description = item.description || '';
    }, [item]);

    return (
        <div>
            <h2>Edit Item</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="name">Name:</label>
                    <input
                        type="text"
                        id="name"
                        name="name"
                        value={liveItem.name}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <label htmlFor="description">Description:</label>
                    <textarea
                        id="description"
                        name="description"
                        value={liveItem.description}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <button
                        type="submit"
                        className='border rounded'
                        disabled={JSON.stringify(savedItem) === JSON.stringify(liveItem)} // Disable button if no changes
                    >
                        Update Item
                    </button>
                </div>
            </form>
            {status && <p>{status}</p>}
        </div>
    );
};

export default ItemComponent;
