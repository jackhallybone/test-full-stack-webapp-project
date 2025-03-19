import { cn } from '@/lib/utils'

type Notification = {
    message: string;
    colour: string;
}

export default function Notifications() {

    const notifications: Notification[] = [
        // { message: "This is an example warning message", colour: "bg-orange-300"},
        // { message: "This is an example error message", colour: "bg-red-300"},
    ]

    return (
        <>
            {notifications.map((notification, index) => (
                <div key={index} className={cn(notification.colour)}>{notification.message}</div>
            ))}
        </>
    );
}