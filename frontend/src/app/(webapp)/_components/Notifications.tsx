import { cn } from '@/app/lib/utils';

type Notification = {
  message: string;
  color: string;
};

export default function Notifications() {
  const notifications: Notification[] = [
    // { message: "This is an example information message", color: "bg-brand-blue" },
    // { message: "This is an example warning message", color: "bg-brand-yellow" },
    // { message: "This is an example error message", color: "bg-brand-red" },
  ];

  return (
    <>
      {notifications.map((notification, index) => (
        <div
          key={index}
          className={cn(
            'text-brand-off-black border-b p-1 text-center font-semibold',
            notification.color
          )}
        >
          {notification.message}
        </div>
      ))}
    </>
  );
}
