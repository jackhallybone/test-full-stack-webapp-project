import { graphQLClient } from "@/app/lib/graphql";
import { gql } from 'graphql-request'
import ItemEditor from "./ItemEditor";

type Item = {
  id: string;
  title: string;
  changelog: string;
  requirements: string;
  outcome: string;
}

type GetItemResponse = {
  item: Item;
}

export default async function DetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  const query = gql`
    query GetItem($id: ID!) {
      item(id: $id) {
        id
        title
        changelog
        requirements
        outcome
      }
    }
  `;
  const variables = { id: id };
  const data: GetItemResponse = await graphQLClient.request(query, variables);

  return (
    <>

      <p className="mb-4">Detail View</p>

      <ItemEditor item={data.item} />

      <p>{JSON.stringify(data)} </p>
    </>
  );
}
