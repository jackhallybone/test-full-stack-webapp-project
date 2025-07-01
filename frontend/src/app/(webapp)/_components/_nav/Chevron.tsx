"use client"

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ChevronRightIcon } from '@heroicons/react/24/outline';
import Title from './Title';
import { cn } from '@/app/lib/utils';


type ChevronProps = {
  tag: 'project' | 'item';
  options: any[];
  labelKey: "name" | "title";
  selected?: string
};

export default function Chevron({ tag, options, labelKey, selected }: ChevronProps) {
  const router = useRouter();
  const [open, setOpen] = useState(false);

  return (
    <div className="relative inline-block">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center focus:outline-none cursor-pointer"
      >
        <ChevronRightIcon
          className={`w-4 h-4 hover:rotate-90 ${open ? 'rotate-90' : ''}`}
        />
      </button>

      {open && (
        <div className="absolute mt-2 w-40 bg-white border rounded shadow-lg">
          <ul>
            {options.map((option) => (
              <li
                key={option.id}
                className={cn(
                  option.id === selected && "text-gray-400 cursor-default pointer-events-none"
                )}
              >
                <Title
                  tag={tag}
                  name={option[labelKey]}
                  id={option.id}
                  className="px-4 py-2 w-full text-left hover:bg-gray-100"
                />
              </li>
            ))}
            <li
              onClick={() => router.push(`/${tag}/create`)}
              className='px-4 py-2 w-full text-left cursor-pointer hover:underline hover:bg-gray-100'
            >
              Create New...
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}
