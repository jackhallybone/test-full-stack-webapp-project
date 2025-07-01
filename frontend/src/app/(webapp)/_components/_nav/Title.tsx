'use client';

import { useRouter } from 'next/navigation';
import { cn } from '@/app/lib/utils';

type TitleProps = {
  tag: 'project' | 'item';
  name: string;
  id?: string;
  className?: string;
};

export default function Title({ tag, name, id, className }: TitleProps) {
  const router = useRouter();

  return (
    <button
      onClick={() => router.push(`/${tag}/${id}`)}
      className={cn("cursor-pointer hover:underline", className)}

    >
      {name}
    </button>
  );
}
