import Button from './_components/Button';

export default function NotFound() {
  return (
    <main className="flex h-screen flex-col justify-center">
      <div className="flex flex-col items-center space-y-4">
        <div className="font-script text-6xl">Thereforeohfour</div>
        <div className="italic">A project management tool with memory, but not for this page.</div>
        <Button href="/" label="Home" className="w-30" />
        <Button href="/dashboard" label="Dashboard" className="w-30" />
      </div>
    </main>
  );
}
