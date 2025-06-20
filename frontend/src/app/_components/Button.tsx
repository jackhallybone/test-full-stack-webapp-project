import Link from 'next/link';

import { cn } from '../lib/utils';

type ButtonProps = {
  href: string;
  label: string;
  className?: string;
};

export default function Button({ href, label, className = '' }: ButtonProps) {
  return (
    <Link
      href={href}
      className={cn(
        'text-brand-off-black bg-brand-light-grey hover:bg-brand-dark-grey ml-1 w-fit cursor-pointer rounded px-2 py-1 text-center',
        className
      )}
    >
      {label}
    </Link>
  );
}
