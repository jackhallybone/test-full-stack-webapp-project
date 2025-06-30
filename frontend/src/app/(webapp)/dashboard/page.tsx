import { graphQLClient } from "@/app/lib/graphql";
import { gql } from 'graphql-request'
import Link from "next/link";

type Children = {
  id: string;
  title: string;
}
type Projects = {
  id: string;
  name: string;
  children: Children[]
}

type GetProjectsResponse = {
  projects: Projects[];
};

export default async function DashboardPage() {

  const query = gql`
    query GetProjects {
      projects {
        id
        name
        children {
          id
          title
        }
      }
    }
  `;
  const data: GetProjectsResponse = await graphQLClient.request(query);

  return (
    <>
      <p>Dashboard</p>
      <p>Projects:</p>
      <ul className="list-disc pl-5 space-y-2">
        {data.projects.map((project) => (
          <li key={project.id}>
            {project.name} ({project.id})
            <ul className="list-disc pl-5 space-y-2">
              {project.children.map((child) => (
                <li key={child.id}>
                  <Link
                    href={`/item/${child.id}`}
                    className="underline"
                  >
                    {child.title} ({child.id})
                  </Link>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>

      <p>{JSON.stringify(data)} </p>
    </>
  );
}
