import Link from 'next/link';

export default function Header() {
  return (
    <div className="mb-4 flex flex-row items-center space-x-2 border-b py-4">
      <Link
        href="/dashboard"
        className="font-script text-brand-off-white dark:text-brand-off-black bg-brand-off-black dark:bg-brand-off-white cursor-pointer rounded px-2 py-1 text-xl"
      >
        Therefore
      </Link>
      <div className="bg-brand-light-grey rounded px-2 py-1 font-mono">[View As]</div>
      <div className="bg-brand-light-grey rounded px-2 py-1 font-mono">[Breadcrumb]</div>
    </div>
  );
}
