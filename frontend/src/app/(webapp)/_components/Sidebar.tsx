import { gql } from 'graphql-request'

import { graphqlRequestClient } from "@/lib/graphqlRequestClient";
import { cn } from '@/lib/utils'
import NavLinks, { LinkItem } from "./NavLinks";

import { RectangleGroupIcon, FolderIcon, Cog6ToothIcon } from '@heroicons/react/24/outline';

type Project = {
    id: string;
    name: string;
}

type GetProjectsResponse = {
    projects: Project[];
};

type SidebarProps = {
    className?: string;
}

export default async function Sidebar({ className }: SidebarProps) {

    const query = gql`
        query GetProjects {
            projects {
                id
                name
            }
        }
    `;
    const data: GetProjectsResponse = await graphqlRequestClient.request(query);

    const links: LinkItem[] = [
        { name: 'Dashboard', href: '/dashboard', icon: <RectangleGroupIcon /> },
        ...data.projects.map((project) => ({
            name: `${project.name}`,
            href: `/project/${project.id}`,  // Correct template string usage
            icon: <FolderIcon />
        })),
        { name: 'Settings', href: '/settings', icon: <Cog6ToothIcon /> },
    ]

    return (
        <div className={cn("p-4 rounded bg-gray-200", className)}>
            <NavLinks links={links} />
        </div>
    );
}