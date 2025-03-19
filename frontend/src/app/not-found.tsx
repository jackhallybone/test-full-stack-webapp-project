import Link from 'next/link'

export default function NotFound() {
  return (
    <div className='flex flex-col'>
        <div>Not Found</div>
        <Link
          href="/"
          className="underline"
        >
          Website Home
        </Link>
        <Link
          href="/dashboard"
          className="underline"
        >
          Dashboard
        </Link>
    </div>
  )
}