import Notifications from './_components/Notifications';
import Header from './_components/Header';
import Sidebar from './_components/Sidebar';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className='h-screen flex flex-col'>
      <Notifications />
      <div className="flex flex-col grow overflow-hidden">
        <Header />
        <div className='flex flex-1 overflow-hidden'>
          <Sidebar className="w-64 m-2 mr-0 overflow-y-auto" />
          <div className='flex-1 m-2 overflow-y-auto break-all'>
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}