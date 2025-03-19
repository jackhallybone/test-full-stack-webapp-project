import Link from "next/link";
import { HomeIcon, RectangleGroupIcon, InformationCircleIcon } from "@heroicons/react/24/outline";

export default function Page() {
    return (
        <main className="h-full flex flex-col items-center text-center justify-center space-y-6">
            <div className="">A project management tool with memory.</div>
            <div className="">Populate your knowledge base directly from the tasks you work on.</div>
            <Link
                href="/dashboard"
                className="bg-gradient-to-r from-pink-500 to-violet-500 font-bold text-white rounded text-lg px-4 py-2 cursor-pointer hover:underline underline-offset-4"
            >
                Dashboard
            </Link>
            <Link
                href="/about"
                className="flex items-center cursor-pointer hover:underline underline-offset-4"
            >
                <InformationCircleIcon className="size-5" />
                <p className="ml-1">About</p>
            </Link>
        </main>
    );
}
