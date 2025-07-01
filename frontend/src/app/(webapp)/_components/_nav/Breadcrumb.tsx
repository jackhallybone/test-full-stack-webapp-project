import { graphQLClient } from "@/app/lib/graphql";
import { gql } from 'graphql-request'
import { HomeIcon } from '@heroicons/react/24/outline';
import Chevron from "./Chevron"
import Title from "./Title";
import React from 'react';

type BreadcrumbProps = {
  tag: "dashboard" | "project" | "item";
  id?: string;
}

type Sibling = {
  id: string;
  title: string;
}
type Children = {
  id: string;
  title: string;
}
type Ancestor = {
  id: string;
  title: string;
  siblings: Sibling[];
}

type Project = {
  id: string;
  name: string;
}

type Item = {
  id: string;
  title: string;
  project: Project;
  ancestors: Ancestor[];
  siblings: Sibling[];
  children: Children[];
}



type GetBreadcrumbsResponse = {
  item: Item;
  projects: Project[];
};

export default async function Breadcrumb({ tag, id }: BreadcrumbProps) {

  const query = gql`
    query GetBreadcrumbs($id: ID!) {
      item(id: $id) {
        id
        title
        project {
          id
          name
        }
        ancestors {
          id
          title
          siblings {
            id
            title
          }
        }
        siblings {
          id
          title
        }
        children {
          id
          title
        }
      }
      projects {
        id
        name
      }
    }
  `;
  const variables = { "id": id }
  const data: GetBreadcrumbsResponse = await graphQLClient.request(query, variables);

  return (
    <>
      <div className="flex flex-row gap-x-2 items-center">
        <HomeIcon className="size-5" />
        <Chevron
          tag="project"
          options={data.projects}
          selected={data.item.project.id}
          labelKey="name"
        />
        <Title
          tag="project"
          name={data.item.project.name}
          id={data.item.project.id}
        />

        {data.item.ancestors.map((ancestor, index) => {
          return (
            <React.Fragment key={index}>
              <Chevron
                tag="item"
                options={[ancestor, ...ancestor.siblings]}
                selected={ancestor.id}
                labelKey="title"
              />
              <Title
                tag="item"
                name={ancestor.title}
                id={ancestor.id}
              />
            </React.Fragment>
          );
        })}

        <Chevron
          tag="item"
          options={[data.item, ...data.item.siblings]}
          selected={data.item.id}
          labelKey="title"
        />
        <Title
          tag="item"
          name={data.item.title}
          id={data.item.id}
        />
        <Chevron
          tag="item"
          options={data.item.children}
          labelKey="title"
        />

        {/* <Drop
          type="item"
          options={data.projects}
          labelKey="title"
        />
        <button className="cursor-pointer hover:underline">Item</button>
        <Drop />
        <button className="cursor-pointer hover:underline">Item</button>
        <Drop />
        <button className="cursor-pointer hover:underline">Item</button> */}
      </div>


      {/* <form className="flex flex-row gap-x-2">
        <Dropdown
          id="project"
          name="project"
          options={data.projects}
          valueKey="id"
          labelKey="name"
          selectedValue={data.item.project.id}
        />

        {data.item.ancestors.map((ancestor, index) => {
          return (
            <Dropdown
              key={ancestor.id}
              id={`ancestor-${index}`}
              name="item"
              options={[ancestor, ...ancestor.siblings]}
              valueKey="id"
              labelKey="title"
              selectedValue={ancestor.id}
            />
          )
        })}

        <Dropdown
          id="item"
          name="item"
          options={[data.item, ...data.item.siblings]}
          valueKey="id"
          labelKey="title"
          selectedValue={data.item.id}
        />
      </form> */}
    </>
  );
}
