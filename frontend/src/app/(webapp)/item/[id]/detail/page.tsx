import { graphQLClient } from "@/app/lib/graphql";
import { gql } from 'graphql-request'
import ItemDetails from "./ItemDetails";
import Breadcrumb from "../../../_components/_nav/Breadcrumb";

type ItemType = {
  id: string;
  name: string;
}
type itemStatus = {
  id: string;
  name: string;
}

type Project = {
  id: string;
  name: string;
}

type ItemLine = {
  id: string;
  itemType: ItemType;
  itemStatus: itemStatus;
  title: string;
  numChildren: string;
}

type Item = {
  id: string;
  itemType: ItemType;
  itemStatus: itemStatus;
  title: string;
  changelog: string;
  requirements: string;
  outcome: string;
  project: Project;
  parent: ItemLine;
  children: ItemLine[];
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
        itemType {
          id
          name
        }
        itemStatus {
          id
          name
        }
        title
        changelog
        requirements
        outcome
        project {
          id
          name
        }
        parent {
          id
          itemType {
            id
            name
          }
          itemStatus {
            id
            name
          }
          title
          numChildren
        }
        children {
          id
          itemType {
            id
            name
          }
          itemStatus {
            id
            name
          }
          title
          numChildren
        }
      }
    }
  `;
  const variables = { id: id };
  const data: GetItemResponse = await graphQLClient.request(query, variables);

  return (
    <>

      <p className="mb-4">Detail View</p>

      <ItemDetails item={data.item} />

      <p>{JSON.stringify(data)} </p>
    </>
  );
}
