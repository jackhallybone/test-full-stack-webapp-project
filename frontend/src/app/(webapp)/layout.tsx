import Notifications from './_components/Notifications';

export default function WebappLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="mx-auto px-2">
      <Notifications />
      {children}
    </div>
  );
}
