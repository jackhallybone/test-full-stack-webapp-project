import { graphqlRequestClient } from "@/lib/graphqlRequestClient";
import { gql } from 'graphql-request'
import ItemComponent from '../../_components/ItemComponent'; // Client-side component for mutation

export default async function Page({
    params,
}: {
    params: Promise<{ id: number }>
}) {
    const id = (await params).id

    const query = gql`
        query GetItem($id: ID!) {
            item(id: $id) {
                id
                name
                description
            }
        }
    `;
    const variables = {
        id: id,
    };
    const data = await graphqlRequestClient.request(query, variables);

    console.log(data);

    return (
        <>
            Details
            <br />
            <ItemComponent item={data.item} />
        </>
    );
}
