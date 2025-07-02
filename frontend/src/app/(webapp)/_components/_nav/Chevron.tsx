"use client"

import { useState } from 'react';
import { ChevronRightIcon } from '@heroicons/react/24/outline';
import Title from './Title';
import { cn } from '@/app/lib/utils';


type ChevronProps = {
  tag: 'project' | 'item';
  options: { id: string; [key: string]: any }[];
  labelKey: "name" | "title";
  selected?: string
};

export default function Chevron({ tag, options, labelKey, selected }: ChevronProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative inline-block">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center focus:outline-none cursor-pointer"
      >
        <ChevronRightIcon
          className={cn("w-4 h-4 transition-transform", open && "rotate-90")}
        />
      </button>

      {open && (
        <div
          className="absolute mt-2 w-40 overflow-hidden border rounded shadow-lg"
          onMouseLeave={() => setOpen(false)}
        >
          <ul role="listbox" tabIndex={-1}>

            {options.map(({ id, ...option }) => {
              const label = option[labelKey];
              const isSelected = id === selected;

              return (
                <li
                  key={id}
                  className={cn(
                    "px-4 py-2 w-full text-left hover:bg-gray-100",
                    isSelected && "text-gray-400 cursor-default pointer-events-none"
                  )}
                >
                  <Title href={`/${tag}/${id}`}>
                    {label}
                  </Title>
                </li>
              );
            })}

            <li className="px-4 py-2 w-full text-left hover:bg-gray-100">
              <Title href={`/${tag}/create`}>
                Create new...
              </Title>
            </li>
          </ul>
        </div>
      )}
    </div>
  );
}
