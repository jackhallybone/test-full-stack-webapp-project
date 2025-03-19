import { graphqlRequestClient } from "@/lib/graphqlRequestClient";
import { gql } from 'graphql-request'
import Link from "next/link";

// TODO: graphql errors too

type Project = {
    id: string;
    name: string;
    description: string;
    children: {
        id: string;
        name: string;
    }[];
}

type GetProjectVariables = {
    id: string;
}

type GetProjectResponse = {
    project: Project;
}

export default async function Page({
    params,
}: {
    params: Promise<{ id: number }>
}) {
    const id = (await params).id

    const query = gql`
        query GetProject($id: ID!) {
            project(id: $id) {
                id
                name
                description
                children {
                    id
                    name
                }
            }
        }
    `;
    const variables: GetProjectVariables = {
        id: String(id),
    };
    const data: GetProjectResponse = await graphqlRequestClient.request(query, variables);

    return (
        <div>
            <p><span className="font-bold">Project ID</span>: {id}</p>
            <p><span className="font-bold">Name</span>: {data.project.name}</p>
            <p><span className="font-bold">Description</span>: {data.project.description}</p>
            {data.project.children.length > 0 ? (
                <>
                    <p><span className="font-bold">Children</span>:</p>
                    <ul className="list-disc list-inside pl-2">
                        {data.project.children.map((child) => (
                            <li key={child.id}>
                                <Link
                                    href={`/item/${child.id}`}
                                    className="underline"
                                >
                                    {child.name}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </>
            ) : (
                <p>No children found.</p>
            )}
        </div>
    );
}