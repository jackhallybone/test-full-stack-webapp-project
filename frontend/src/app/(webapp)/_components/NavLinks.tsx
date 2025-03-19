'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';

import { cn } from '@/lib/utils'

import React, { ReactElement, SVGProps } from 'react';


export type LinkItem = {
    name: string;
    href: string;
    icon: ReactElement<SVGProps<SVGSVGElement>>;
}

type NavLinksProps = {
    links: LinkItem[];
}

export default function NavLinks({ links }: NavLinksProps) {
    const pathname = usePathname();

    return (
        <>
            {links.map((link, index) => {
                return (
                    <Link
                        key={index}
                        href={link.href}
                        className={cn(
                            "flex items-center my-2 rounded p-1 hover:bg-gray-300",
                            {
                                'bg-gray-300': pathname === link.href,
                            }
                        )}
                    >
                        {React.cloneElement(link.icon, { className: "size-5 mr-2" })}
                        <p>{link.name}</p>
                    </Link>
                );
            })}
        </>
    );
}