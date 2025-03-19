'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';

import { BookOpenIcon, QueueListIcon, ViewColumnsIcon, CalendarIcon, DocumentIcon } from '@heroicons/react/24/outline';

import { cn } from '@/lib/utils'

export default function ViewBar({ id }: { id: string; }) {
    const pathname = usePathname();

    const links = [
        { name: 'Details', href: '', icon: BookOpenIcon },
        { name: 'Backlog', href: '/backlog', icon: QueueListIcon },
        { name: 'Kanban', href: '/kanban', icon: ViewColumnsIcon },
        { name: 'Gantt', href: '/gantt', icon: CalendarIcon },
        { name: 'Document', href: '/document', icon: DocumentIcon },
    ]

    return (
        <div className="flex flex-row gap-2 mb-2 bg-red-50">
            {links.map((link, index) => {
                const href = `/item/${id}${link.href}`;
                return (
                    <Link
                        key={index}
                        href={href}
                        className={cn(
                            "grow flex items-center rounded p-1 border hover:bg-gray-300",
                            {
                                'bg-gray-300': pathname === href,
                            }
                        )}
                    >
                        <link.icon className="size-5 mr-2" />
                        <p>{link.name}</p>
                    </Link>

                );
            })}
        </div>
    );
}