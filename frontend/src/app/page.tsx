import Button from './_components/Button';

export default function HomePage() {
  return (
    <main className="flex h-screen flex-col justify-center">
      <div className="flex flex-col items-center space-y-4">
        <h1 className="font-script text-6xl">Therefore</h1>
        <div className="font-semibold italic">A project management tool with memory.</div>
        <div className="">Populate your knowledge base directly from the tasks you work on.</div>
        <Button href="/dashboard" label="Take Me There!" />

        <div className="m-2 flex flex-col space-y-2 rounded border p-2 font-mono">
          <div className="bg-brand-white text-brand-off-black rounded px-2 py-1">brand-white</div>
          <div className="bg-brand-off-white text-brand-off-black rounded px-2 py-1">
            brand-off-white
          </div>
          <div className="bg-brand-black text-brand-off-white rounded px-2 py-1">brand-black</div>
          <div className="bg-brand-off-black text-brand-off-white rounded px-2 py-1">
            brand-off-black
          </div>
          <div className="bg-brand-light-grey text-brand-off-black rounded px-2 py-1">
            brand-light-grey
          </div>
          <div className="bg-brand-dark-grey text-brand-off-black rounded px-2 py-1">
            brand-dark-grey
          </div>
          <div className="bg-brand-terracotta rounded px-2 py-1">brand-terracotta</div>
          <div className="bg-brand-blue rounded px-2 py-1">brand-blue</div>
          <div className="bg-brand-red rounded px-2 py-1">brand-red</div>
          <div className="bg-brand-yellow rounded px-2 py-1">brand-yellow</div>
          <div className="bg-brand-green rounded px-2 py-1">brand-green</div>
        </div>
      </div>
    </main>
  );
}
