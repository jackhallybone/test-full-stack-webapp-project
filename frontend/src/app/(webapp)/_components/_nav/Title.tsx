import Link from 'next/link';
import { cn } from '@/app/lib/utils';

type TitleProps = {
  href: string;
  children: React.ReactNode;
  className?: string;
};

export default function Title({ href, children, className = "" }: TitleProps) {
  return (
    <Link href={href} className={cn("inline-block cursor-pointer hover:underline", className)}>
      {children}
    </Link>
  );
}
