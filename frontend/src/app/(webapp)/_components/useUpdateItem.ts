// hooks/useUpdateItem.ts
import { useState } from 'react';
import { graphqlRequestClient } from "@/lib/graphqlRequestClient";
import { gql } from 'graphql-request';

const mutation = gql`
    mutation UpdateItem($id: ID!, $input: PartialUpdateItemInput!) {
        updateItem(id: $id, input: $input) {
            item {
                name
                description
            }
        }
    }
`;

export const useUpdateItem = (initialItem) => {
    const [savedItem, setSavedItem] = useState({
        name: initialItem.name || '',
        description: initialItem.description || '',
    });
    const [liveItem, setLiveItem] = useState({
        name: initialItem.name || '',
        description: initialItem.description || '',
    });
    const [status, setStatus] = useState(''); // To show success or error messages

    const handleChange = (e) => {
        const { name, value } = e.target;
        setLiveItem((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Compare savedItem and liveItem to determine changes
        const changes = {};
        for (const key in liveItem) {
            if (liveItem[key] !== savedItem[key]) {
                changes[key] = liveItem[key];
            }
        }

        if (Object.keys(changes).length === 0) {
            setStatus('No changes made.');
            return;
        }

        setStatus('Updating...');

        try {
            const variables = {
                id: initialItem.id,
                input: changes,
            };

            const response = await graphqlRequestClient.request(mutation, variables);

            if (response.updateItem) {
                setStatus('Item updated successfully!');
                setSavedItem(liveItem); // Update savedItem to reflect the current state
            } else {
                setStatus('Failed to update item.');
            }
        } catch (error) {
            console.error('Error updating item:', error);
            setStatus('Error updating item.');
        }
    };

    return {
        savedItem,
        liveItem,
        status,
        handleChange,
        handleSubmit
    };
};
