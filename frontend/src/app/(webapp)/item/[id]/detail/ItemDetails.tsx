'use client';

import { graphQLClient } from "@/app/lib/graphql";
import { gql } from 'graphql-request'
import { AutoSaveField } from './AutoSaveField';

export default function ItemDetails({ item }: { item: Item }) {

  async function saveField(fieldName: keyof Item, value: string) {
    const mutation = gql`
      mutation UpdateItem($id: ID!, $input: UpdateItemInput!) {
        updateItem(id: $id, input: $input) {
          item { id }
        }
      }
    `;
    await graphQLClient.request(mutation, {
      id: item.id,
      input: { [fieldName]: value },
    });
  }

  return (
    <>
      <AutoSaveField
        id="title"
        label="Title"
        initialValue={item.title}
        type="input"
        onSave={val => saveField('title', val)}
      />
      <AutoSaveField
        id="changelog"
        label="Changelog"
        initialValue={item.changelog}
        type="input"
        onSave={val => saveField('changelog', val)}
      />
      <AutoSaveField
        id="requirements"
        label="Requirements"
        initialValue={item.requirements}
        type="textarea"
        onSave={val => saveField('requirements', val)}
      />
      <AutoSaveField
        id="outcome"
        label="Outcome"
        initialValue={item.outcome}
        type="textarea"
        onSave={val => saveField('outcome', val)}
      />
    </>
  );
}
